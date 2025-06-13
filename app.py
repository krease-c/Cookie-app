from flask import Flask, request, redirect, make_response, render_template_string

app = Flask(__name__)

FLAG = "ctf{super_secret_flag}"

# HTML template for login form and admin page
LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <h2>Login</h2>
    <form method="post" action="/login">
        Username: <input name="username" /><br>
        Password: <input name="password" type="password" /><br>
        <input type="submit" value="Login" />
    </form>
    {% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
</body>
</html>
"""

ADMIN_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Admin</title></head>
<body>
    <h2>Welcome, admin!</h2>
    <p>Here is your flag: <b>{{ flag }}</b></p>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == "admin" and password == "password123":
            # Login is accepted but not admin
            resp = make_response(redirect("/admin"))
            resp.set_cookie("admin", "false")  # Only manual tampering will work
            return resp
        else:
            return render_template_string(LOGIN_PAGE, error="Invalid credentials")
    return render_template_string(LOGIN_PAGE, error=None)

@app.route("/admin")
def admin():
    admin_cookie = request.cookies.get("admin", "false")
    if admin_cookie == "true":
        return render_template_string(ADMIN_PAGE, flag=FLAG)
    return "Access denied. You are not admin.", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
