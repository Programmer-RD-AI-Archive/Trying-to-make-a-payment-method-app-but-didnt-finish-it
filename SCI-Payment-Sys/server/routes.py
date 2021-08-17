from server import *
from datetime import date
import pandas as pd
import simplify

simplify.public_key = ""
simplify.private_key = (
    ""
)


@app.route("/", methods=["POST", "GET"])
def pay():
    if request.method == "POST":
        student_id = request.form["SI"]
        name = request.form["N"]
        phone_num = request.form["PN"]
        grade = request.form["G"]
        subject = request.form["S"]
        amount = request.form["A"]
        month = request.form["M"]
        description = request.form["D"]
        card_number = request.form["CN"]
        exp = request.form["E"]
        print(exp)
        cvc = request.form["CVC"]
        data = pd.read_csv("./server/logs.csv")
        data = data.append(
            {
                "date": date.today(),
                "student_id": student_id,
                "name": name,
                "whatsapp": phone_num,
                "grade": grade,
                "subject": subject,
                "amount": amount,
                "month": month,
                "description": description,
            },
            ignore_index=True,
        )
        data.to_csv("./server/logs.csv", index=False)
        exp = exp.split("-")
        payment = simplify.Payment.create(
            {
                "card": {
                    "number": card_number,
                    "expMonth": exp[1],
                    "expYear": exp[0],
                    "cvc": cvc,
                },
                "amount": amount,
                "description": description,
                "currency": "LKR",
            }
        )
        if payment.paymentStatus == "APPROVED":
            pay_result = True
        else:
            pay_result = False
        if pay_result is False:
            flash("transaction is not complete", "danger")
            return redirect("/")
        flash(
            f"OK Done you can send a picture of this text to SCI whatapp number 0774045614 ({student_id},{name})",
            "success",
        )
        return redirect("/")
    else:
        return render_template("/pay.html")


@app.route("/admin", methods=["POST", "GET"])
def admin():
    if request.method == "POST":
        user_name = request.form["UN"]
        password = request.form["P"]
        if user_name == "ranugad2008" and password == "PROGRAMMER-RD-AI":
            session["ok"] = True
            return redirect("/admin/download")
        return ":("
    else:
        return render_template("/admin_login.html")


@app.route("/admin/download", methods=["POST", "GET"])
def admin_download():
    if session["ok"] is True:
        print(session["ok"])
        return send_from_directory(
            filename="logs.csv",
            directory="/home/indika/Programming/Projects/Python/Web-Dev/SCI-Payment-Sys/server",
            as_attachment=True,
        )
    return ":("
