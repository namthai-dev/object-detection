import { useState, useEffect } from 'react';
import './App.css';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';


function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [predictedImage, setPredictedImage] = useState(null);
  const [taskId, setTaskId] = useState(null);

  const onSubmit = () => {
    const formData = new FormData();
    formData.append('img', selectedImage);

    fetch("http://localhost:8001/detect/", {
      method: "POST",
      body: formData,
    }).then((res) => res.json())
      .then(data => setTaskId(data))
  }

  const getPredictedImage = () => {
    fetch("http://localhost:8001/detect/status/" + taskId, {
      method: "GET",
    }).then((res) => res.json())
      .then(data => {
        if (data === "ok") {
          setPredictedImage("http://localhost:8001/detect/image/" + taskId)
          setTaskId(null)
        } else {
          window.setTimeout(() => getPredictedImage(), 1000)
        }
      })
  }
  useEffect(() => {
    if (taskId !== null) {
      getPredictedImage()
    }
  }, [taskId])

  return (
    <Container className="p-3">
      <Container className="p-5 mb-4 bg-light rounded-3">
        <h1 className="header">Object detection project</h1>
        <div className="mb-4">
          {selectedImage && (
            <div>
              <img
                alt="not found"
                src={URL.createObjectURL(selectedImage)}
              />
              <br />
              <button onClick={() => setSelectedImage(null)}>Remove</button>
            </div>
          )}
          <br />
          <br />
          <input
            type="file"
            name="myImage"
            onChange={(event) => {
              setSelectedImage(event.target.files[0]);
            }}
          />
        </div>
        {selectedImage && <Button onClick={onSubmit}>Submit</Button>}
        {taskId && <p className="mt-4">Submitted task with id={taskId}. Please wait.</p>}
        <div>
          {predictedImage && (
            <div>
              <h2 className="mt-4">Predicted image</h2>
              <img
                alt="not found"
                src={predictedImage}
              />
              <br />
              <button onClick={() => {
                setPredictedImage(null)
                setSelectedImage(null)
              }}>Restart</button>
            </div>
          )}
        </div>
      </Container>
    </Container>
  );
}

export default App;
