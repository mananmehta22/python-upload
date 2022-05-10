import React from 'react';

class Main extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      URL: '',
    };

    this.handleUpload = this.handleUpload.bind(this);
  }

  handleUpload(ev) {
    ev.preventDefault();

    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);
    data.append('filename', this.fileName.value);

    fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: data,
      headers: {
        'Access-Control-Allow-Origin': "*"}
    }).then((response) => response.json())
    .then((result) => {
      console.log('Success:', result);
    })
    .then((body) => {
      this.setState({ URL: `http://localhost:5000/${body.file}` });
    })
    .catch((error) => {
      console.error('Error:', error);
    });
    
    
  }

  render() {
    return (
      <form onSubmit={this.handleUpload}>
        <div>
          <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
        </div>
        <div>
          <input ref={(ref) => { this.fileName = ref; }} type="text" placeholder="Enter the desired name of file" />
        </div>
        <br />
        <div>
          <button>Upload</button>
        </div>
      </form>
    );
  }
}

export default Main;