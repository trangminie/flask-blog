from flask import Flask, render_template, request
import requests
import smtplib

app = Flask(__name__)
response = requests.get("https://api.npoint.io/e810d59e6ed4856aa62a").json()

MY_EMAIL = "fxkrytal.trangbui@funix.edu.vn"
PASSWORD = "Funix@2022"


@app.route("/")
def home():
    return render_template("index.html", data=response)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    msg = "Contact Me"
    if request.method == 'POST':
        name = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        email_msg = f"From: {name}\n Address: {email}\n Phone number: {phone}\n Message: {message}"

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.ehlo()
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="trangminie@gmail.com",
                msg=f"Subject:You have new message\n\n{email_msg}"
            )

        msg = "Successfully sent message"

    return render_template("contact.html", send_msg=msg)



@app.route("/post/<int:blog_id>")
def blog_post(blog_id):
    blog = None
    for item in response:
        if item["id"] == blog_id:
            blog = item
            break
    print(blog_id)
    return render_template("post.html", title=blog["title"], subtitle=blog["subtitle"], body=blog["body"])




if __name__ == "__main__":
    app.run(debug=True)