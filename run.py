from dental_clinic_app import app
import webbrowser

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/login')
    app.run(debug=True)