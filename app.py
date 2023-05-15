from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import cv2
import base64
import dash

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1(
            "Face Recognition API",
            style={"color": "black", "text-align": "center"},
        ),
        html.Div(
            [
                dcc.Upload(
                    id="upload-image",
                    children=html.Button("Select Image"),
                    style={
                        "width": "180",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "backgroundColor": "black",
                    },
                    multiple=False,
                )
            ],
            style={
                "display": "flex",
                "justify-content": "center",
                "margin": "10px",
            },
        ),
        html.Img(
            id="output-image",
            style={
                "width": "55%",
                "margin": "10px",
                "display": "block",
                "margin-left": "auto",
                "margin-right": "auto",
            },
        ),
        html.Div(
            id="output-result",
            style={
                "font-size": "20px",
                "text-align": "center",
                "margin": "10px",
                "color": "black",
            },
        ),
    ],
    style={"backgroundColor": "blue"}  # Set the background color to pink
)


def detect_faces(image_path):
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    result_path = "result.jpg"
    cv2.imwrite(result_path, img)
    return result_path, len(faces)


@app.callback(
    [Output("output-image", "src"), Output("output-result", "children")],
    [Input("upload-image", "contents")],
    [State("upload-image", "filename")],
)
def update_output(image, filename):
    if image is not None:
        image_decoded = base64.b64decode(image.split(",")[1])
        with open(filename, "wb") as f:
            f.write(image_decoded)
        result_path, num_faces = detect_faces(filename)
        result_encoded = base64.b64encode(open(result_path, "rb").read()).decode()
        return (
            "data:image/jpeg;base64,{}".format(result_encoded),
            "Number of faces detected: {}".format(num_faces),
        )
    else:
        return None, None


if __name__ == "__main__":
    app.run_server(debug=True)









