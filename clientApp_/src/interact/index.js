import React, { Component } from "react";

//
class Userland extends Component {
  constructor() {
    super();

    this.state = {
      text: null
    };
  }

  onTextChange = event => {
    this.setState({
      ...this.state,
      text: event.target.value
    });

    console.log(this.state.text);
  };

  onButtonClick = () => {
    //prepare your post here which comes
    console.log("we will post this text now", this.state.text);
  };

  render() {
    return (
      <>
        <form>
          <input onChange={this.onTextChange} type="text" />
          <button type="button" onClick={this.onButtonClick}>
            press here
          </button>
        </form>
      </>
    );
  }
}

export default Userland;
