from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from decimal import Decimal
from src.ledger import Ledger, Posting
from src.merkle import hex_root
from src.routing import GraphRouter
from src.segment_tree import SegmentTree
from src.fraud_graph import DSU
from src.atm_dp import min_notes
import uuid
from datetime import datetime, timedelta
import random
import json
import csv
from io import StringIO
from flask import make_response
import os
import secrets

app = Flask(__name__)
# Security: Use environment variable for secret key, generate random for dev
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Security: Configure secure session cookies
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Security: Enforce HTTPS - Redirect HTTP to HTTPS
@app.before_request
def force_https():
    """Redirect HTTP to HTTPS in production - Render automatically does this, but this ensures it"""
    if os.environ.get('FLASK_ENV') == 'production':
        # Render sets X-Forwarded-Proto header, check that
        forwarded_proto = request.headers.get('X-Forwarded-Proto', '')
        # If it's explicitly HTTP, redirect to HTTPS
        if forwarded_proto == 'http':
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)
        # Also check if request URL is HTTP
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)

# Security: Add security headers
@app.after_request
def set_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    if os.environ.get('FLASK_ENV') == 'production':
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data: https:;"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response

# Global instances
ledger = Ledger()
fraud_detector = DSU()
router = GraphRouter()
interest_tree = SegmentTree(100)  # Support up to 100 days

# Create system account for initial deposits (double-entry requirement)
system_account = ledger.create_account()

# Initialize demo accounts with realistic account numbers
demo_accounts = {}
account_names = {}
for i in range(3):
    acc_id = ledger.create_account()
    # Format as realistic account number (12 digits)
    formatted_id = acc_id.replace('-', '')[:12].upper()
    demo_accounts[f"account_{i+1}"] = acc_id
    account_names[acc_id] = f"Checking Account ****{formatted_id[-4:]}"
    # Set initial balance to 50,000 EUR for new users
    initial_balance = Decimal("50000")
    # Create an initial deposit transaction - must sum to zero
    try:
        ledger.post([
            Posting(system_account, Decimal("-1") * initial_balance),
            Posting(acc_id, initial_balance)
        ], metadata={'desc': 'Initial Deposit', 'timestamp': datetime.now().isoformat()})
    except Exception as e:
        # If posting fails, manually set balance (for demo purposes)
        ledger.caccounts[acc_id] = initial_balance
    fraud_detector.add(acc_id)

# Initialize routing graph
router.add_edge("BankA", "BankB", 3)
router.add_edge("BankB", "BankC", 2)
router.add_edge("BankA", "BankC", 10)
router.add_edge("BankC", "BankD", 1)

@app.route('/test')
def test():
    """Simple test route to verify server is working"""
    return "<h1>Server is working! <a href='/login'>Go to Login</a></h1>"

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return app.send_static_file('favicon.svg'), 200, {'Content-Type': 'image/svg+xml'}

@app.route('/favicon.svg')
def favicon_svg():
    """Serve favicon SVG"""
    return app.send_static_file('favicon.svg'), 200, {'Content-Type': 'image/svg+xml'}

@app.route('/')
def index():
    try:
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple demo authentication (in production, use proper auth)
        if username and password:
            session['user_id'] = username
            
            # Check if user already has an account, otherwise create new one with 50,000 EUR
            user_account_key = f"user_{username}"
            if user_account_key not in demo_accounts:
                # Create new account for user with 50,000 EUR
                acc_id = ledger.create_account()
                formatted_id = acc_id.replace('-', '')[:12].upper()
                demo_accounts[user_account_key] = acc_id
                account_names[acc_id] = f"Checking Account ****{formatted_id[-4:]}"
                
                # Set initial balance to 50,000 EUR
                initial_balance = Decimal("50000")
                try:
                    ledger.post([
                        Posting(system_account, Decimal("-1") * initial_balance),
                        Posting(acc_id, initial_balance)
                    ], metadata={'desc': 'Welcome Bonus - Initial Deposit', 'timestamp': datetime.now().isoformat()})
                except Exception as e:
                    ledger.caccounts[acc_id] = initial_balance
                fraud_detector.add(acc_id)
            
            session['account_id'] = demo_accounts[user_account_key]
            return redirect(url_for('dashboard'))
    
    # Clear any existing session when showing login
    if 'user_id' in session:
        session.pop('user_id', None)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    account_id = session.get('account_id')
    
    # Ensure account exists, create if needed
    if account_id and account_id not in ledger.caccounts:
        # Account doesn't exist, create new one with 50,000 EUR
        initial_balance = Decimal("50000")
        try:
            ledger.post([
                Posting(system_account, Decimal("-1") * initial_balance),
                Posting(account_id, initial_balance)
            ], metadata={'desc': 'Welcome Bonus - Initial Deposit', 'timestamp': datetime.now().isoformat()})
        except Exception as e:
            ledger.caccounts[account_id] = initial_balance
        if account_id not in account_names:
            formatted_id = account_id.replace('-', '')[:12].upper()
            account_names[account_id] = f"Checking Account ****{formatted_id[-4:]}"
    
    # Get balance safely
    try:
        balance = ledger.balance(account_id) if account_id else Decimal("0")
    except KeyError:
        balance = Decimal("0")
        if account_id:
            ledger.caccounts[account_id] = Decimal("50000")
            balance = Decimal("50000")
    
    # Format account number for display
    account_number = account_id[:8] if account_id else "00000000"
    account_display = account_names.get(account_id, f"Account ****{account_number[-4:]}")
    
    # Get all account balances for display
    all_accounts = ledger.all_accounts()
    
    # Get recent transactions count
    recent_count = len([e for e in ledger.centries if account_id and any(p.account_id == account_id for p in e.postings)])
    
    return render_template('dashboard.html', 
                         balance=balance, 
                         account_id=account_id,
                         account_display=account_display,
                         account_number=account_number,
                         accounts=all_accounts,
                         transaction_count=recent_count)

@app.route('/api/balance')
def api_balance():
    if 'account_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    account_id = session.get('account_id')
    balance = ledger.balance(account_id)
    return jsonify({'balance': str(balance), 'account_id': account_id[:8]})

@app.route('/api/transfer', methods=['POST'])
def api_transfer():
    if 'account_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    from_account = session.get('account_id')
    to_account = data.get('to_account')
    
    # Input validation and sanitization
    if not to_account or not isinstance(to_account, str):
        return jsonify({'error': 'Invalid recipient account'}), 400
    
    try:
        amount = Decimal(str(data.get('amount', 0)))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid amount format'}), 400
    
    if amount <= 0:
        return jsonify({'error': 'Invalid amount'}), 400
    
    try:
        # Check if recipient exists (for demo, use first available account if not found)
        if to_account not in ledger.all_accounts():
            # Create account if doesn't exist
            ledger.caccounts[to_account] = Decimal("0")
            fraud_detector.add(to_account)
            account_names[to_account] = f"Account ****{to_account[-4:]}"
        
        # Get recipient name for description
        recipient_name = account_names.get(to_account, f"Account ****{to_account[-4:]}")
        
        ledger.post([
            Posting(from_account, -amount),
            Posting(to_account, amount)
        ], metadata={
            'desc': f'Transfer to {recipient_name}',
            'from': from_account,
            'to': to_account,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True, 
            'message': f'Transfer of €{amount:,.2f} to {recipient_name} completed successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/transactions')
def api_transactions():
    if 'account_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    account_id = session.get('account_id')
    transactions = []
    
    # Generate timestamps (for demo, use entry index to create realistic dates)
    base_date = datetime.now()
    
    for idx, entry in enumerate(reversed(ledger.centries)):
        for posting in entry.postings:
            if posting.account_id == account_id:
                # Create realistic timestamp (more recent first)
                days_ago = idx * 2
                tx_date = (base_date - timedelta(days=days_ago))
                
                # Determine transaction type and counterparty
                amount = posting.amount
                desc = entry.metadata.get('desc', 'Transaction')
                
                # Get counterparty account
                counterparty = None
                for p in entry.postings:
                    if p.account_id != account_id:
                        counterparty = account_names.get(p.account_id, f"Account ****{p.account_id[-4:]}")
                
                transactions.append({
                    'id': entry.entry_id[:8],
                    'amount': str(amount),
                    'description': desc,
                    'counterparty': counterparty or 'External',
                    'date': tx_date.strftime('%Y-%m-%d'),
                    'time': tx_date.strftime('%H:%M'),
                    'datetime': tx_date.isoformat(),
                    'type': 'debit' if amount < 0 else 'credit',
                    'status': 'Completed'
                })
    
    # Sort by date (most recent first)
    transactions.sort(key=lambda x: x['datetime'], reverse=True)
    
    return jsonify({'transactions': transactions})

@app.route('/transactions')
def transactions_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('transactions.html')

@app.route('/tools/atm')
def atm_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('atm.html')

@app.route('/api/atm', methods=['POST'])
def api_atm():
    data = request.json
    amount = int(data.get('amount', 0))
    notes = [500, 200, 100, 50, 20, 10]
    counts = [10, 10, 10, 10, 10, 10]  # Available counts
    
    result = min_notes(amount, notes, counts)
    return jsonify({
        'amount': amount,
        'min_notes': result,
        'notes_available': dict(zip(notes, counts))
    })

@app.route('/tools/routing')
def routing_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('routing.html')

@app.route('/api/routing', methods=['POST'])
def api_routing():
    data = request.json
    start = data.get('start')
    end = data.get('end')
    
    cost, path = router.shortest_path(start, end)
    
    return jsonify({
        'cost': cost if cost != float('inf') else None,
        'path': path,
        'success': cost != float('inf')
    })

@app.route('/tools/fraud')
def fraud_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('fraud.html')

@app.route('/api/fraud/check', methods=['POST'])
def api_fraud_check():
    data = request.json
    account1 = data.get('account1')
    account2 = data.get('account2')
    
    if account1 not in fraud_detector.cpar or account2 not in fraud_detector.cpar:
        return jsonify({'error': 'Account not found'}), 400
    
    connected = fraud_detector.connected(account1, account2)
    return jsonify({'connected': connected})

@app.route('/tools/fraud/link', methods=['POST'])
def api_fraud_link():
    data = request.json
    account1 = data.get('account1')
    account2 = data.get('account2')
    
    if account1 not in fraud_detector.cpar:
        fraud_detector.add(account1)
    if account2 not in fraud_detector.cpar:
        fraud_detector.add(account2)
    
    merged = fraud_detector.union(account1, account2)
    return jsonify({'merged': merged, 'message': 'Accounts linked'})

# ===== Statement Download Routes =====
@app.route('/statement')
def statement_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('statement.html')

@app.route('/api/statement', methods=['POST'])
def api_statement():
    if 'account_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    account_id = session.get('account_id')
    month = data.get('month')
    year = data.get('year')
    
    transactions = []
    base_date = datetime.now()
    
    for idx, entry in enumerate(reversed(ledger.centries)):
        for posting in entry.postings:
            if posting.account_id == account_id:
                tx_date = (base_date - timedelta(days=idx * 2))
                if month and tx_date.month != int(month):
                    continue
                if year and tx_date.year != int(year):
                    continue
                
                counterparty = None
                for p in entry.postings:
                    if p.account_id != account_id:
                        counterparty = account_names.get(p.account_id, f"Account ****{p.account_id[-4:]}")
                
                transactions.append({
                    'date': tx_date.strftime('%Y-%m-%d'),
                    'description': entry.metadata.get('desc', 'Transaction'),
                    'counterparty': counterparty or 'External',
                    'debit': str(abs(posting.amount)) if posting.amount < 0 else '',
                    'credit': str(posting.amount) if posting.amount > 0 else '',
                    'balance': str(ledger.balance(account_id))
                })
    
    return jsonify({'transactions': transactions})

@app.route('/api/statement/download')
def download_statement():
    if 'account_id' not in session:
        return redirect(url_for('login'))
    
    account_id = session.get('account_id')
    month = request.args.get('month')
    year = request.args.get('year')
    
    # Generate CSV
    output = StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Date', 'Description', 'Counterparty', 'Debit', 'Credit', 'Balance'])
    
    base_date = datetime.now()
    for idx, entry in enumerate(reversed(ledger.centries)):
        for posting in entry.postings:
            if posting.account_id == account_id:
                tx_date = (base_date - timedelta(days=idx * 2))
                if month and tx_date.month != int(month):
                    continue
                if year and tx_date.year != int(year):
                    continue
                
                counterparty = None
                for p in entry.postings:
                    if p.account_id != account_id:
                        counterparty = account_names.get(p.account_id, f"Account ****{p.account_id[-4:]}")
                
                writer.writerow([
                    tx_date.strftime('%Y-%m-%d'),
                    entry.metadata.get('desc', 'Transaction'),
                    counterparty or 'External',
                    abs(posting.amount) if posting.amount < 0 else '',
                    posting.amount if posting.amount > 0 else '',
                    ledger.balance(account_id)
                ])
    
    response = make_response(output.getvalue())
    filename = f"statement_{year or 'all'}_{month or 'all'}.csv"
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    response.headers['Content-type'] = 'text/csv'
    return response

# ===== Loans Routes =====
@app.route('/loans')
def loans_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    loan_types = [
        {'name': 'Personal Loan', 'interest': '10.5%', 'min_amount': 50000, 'max_amount': 500000, 'tenure': '1-5 years'},
        {'name': 'Home Loan', 'interest': '8.75%', 'min_amount': 500000, 'max_amount': 10000000, 'tenure': '5-30 years'},
        {'name': 'Car Loan', 'interest': '9.25%', 'min_amount': 100000, 'max_amount': 2000000, 'tenure': '1-7 years'},
        {'name': 'Education Loan', 'interest': '8.5%', 'min_amount': 100000, 'max_amount': 4000000, 'tenure': '1-15 years'},
        {'name': 'Business Loan', 'interest': '11.5%', 'min_amount': 100000, 'max_amount': 5000000, 'tenure': '1-10 years'},
    ]
    
    return render_template('loans.html', loan_types=loan_types)

# ===== Services Routes =====
@app.route('/services')
def services_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('services.html')

@app.route('/api/payee/add', methods=['POST'])
def api_add_payee():
    if 'account_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    # In real app, store in database
    return jsonify({'success': True, 'message': 'Payee added successfully'})

@app.route('/api/recharge', methods=['POST'])
def api_recharge():
    if 'account_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    amount = Decimal(str(data.get('amount', 0)))
    phone = data.get('phone')
    
    account_id = session.get('account_id')
    try:
        # Recharge should debit from account
        ledger.post([
            Posting(account_id, -amount),
            Posting(system_account, amount)
        ], metadata={'desc': f'Mobile Recharge - {phone}', 'timestamp': datetime.now().isoformat()})
        return jsonify({'success': True, 'message': f'Recharge of €{amount} successful'})
    except:
        return jsonify({'error': 'Transaction failed'}), 400

@app.route('/api/billpay', methods=['POST'])
def api_billpay():
    if 'account_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    amount = Decimal(str(data.get('amount', 0)))
    biller = data.get('biller')
    
    account_id = session.get('account_id')
    try:
        ledger.post([
            Posting(account_id, -amount),
            Posting(system_account, amount)
        ], metadata={'desc': f'Bill Payment - {biller}', 'timestamp': datetime.now().isoformat()})
        return jsonify({'success': True, 'message': f'Bill payment of €{amount} successful'})
    except:
        return jsonify({'error': 'Payment failed'}), 400

# ===== Investments Routes =====
@app.route('/investments')
def investments_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    investment_types = [
        {'name': 'Fixed Deposit', 'interest': '6.5%', 'min_amount': 10000, 'tenure': '1-10 years', 'type': 'FD'},
        {'name': 'Recurring Deposit', 'interest': '6.0%', 'min_amount': 1000, 'tenure': '6 months - 10 years', 'type': 'RD'},
        {'name': 'Tax Saver Deposit', 'interest': '7.0%', 'min_amount': 100000, 'tenure': '5 years', 'type': 'TSD'},
    ]
    
    return render_template('investments.html', investment_types=investment_types)

@app.route('/api/investment/open', methods=['POST'])
def api_open_investment():
    if 'account_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    inv_type = data.get('type')
    amount = Decimal(str(data.get('amount', 0)))
    
    # In real app, create investment account
    return jsonify({'success': True, 'message': f'{inv_type} opened with €{amount}'})

# ===== Cards Routes =====
@app.route('/cards')
def cards_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('cards.html')

@app.route('/api/card/order', methods=['POST'])
def api_order_card():
    if 'account_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    card_type = data.get('type', 'standard')
    # In real app, create card order
    return jsonify({
        'success': True,
        'message': f'{card_type} card ordered successfully'
    })

# ===== Profile Routes =====
@app.route('/profile')
def profile_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    account_id = session.get('account_id')
    balance = ledger.balance(account_id)
    
    user_data = {
        'username': session.get('user_id'),
        'account_number': account_names.get(account_id, 'N/A'),
        'balance': balance,
        'member_since': '2025-01-01',
        'email': f"{session.get('user_id')}@algobank.com",
        'phone': '***-***-****'
    }
    
    return render_template('profile.html', user_data=user_data)

if __name__ == '__main__':
    import os
    # Production-ready configuration
    port = int(os.environ.get('PORT', 8080))  # Use 8080 instead of 5000 to avoid AirPlay conflict
    host = os.environ.get('HOST', '0.0.0.0')  # Listen on all interfaces for production
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # For production, disable debug mode
    if os.environ.get('FLASK_ENV') == 'production':
        debug = False
    
    app.run(debug=debug, host=host, port=port)

