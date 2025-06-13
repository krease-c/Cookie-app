from flask import Flask, request, redirect, render_template, make_response

app = Flask(__name__)

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        resp = make_response(redirect('/admin'))
        resp.set_cookie('role', 'guest')
        return resp
    return render_template('login.html')

@app.route('/admin')
def admin():
    role = request.cookies.get('role')
    if role == 'admin':
        with open('flag.txt') as f:
            flag = f.read()
        return render_template('admin.html', flag=flag)
    else:
        return "Access denied: You must be an admin."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
