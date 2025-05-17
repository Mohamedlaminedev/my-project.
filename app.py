from flask import Flask, render_template, request, send_file
import qrcode
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_image = None
    error = None
    if request.method == 'POST':
        data = request.form.get('data')
        if data:
            try:
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(data)
                qr.make(fit=True)
                img = qr.make_image(fill='black', back_color='white')
                
                # Use in-memory buffer
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                buffer.seek(0)

                # Send the image as a file response
                return send_file(buffer, mimetype='image/png')
            except Exception:
                error = "Invalid input. Please enter a valid link or text."
        else:
            error = "Please enter a link or text."
    return render_template('index.html', qr_image=qr_image, error=error)

if __name__ == "__main__":
    app.run(debug=True)
