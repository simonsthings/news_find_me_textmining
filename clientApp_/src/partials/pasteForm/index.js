import React, { Component } from "react";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";

import Plot from "../../components/plot";
import KeyWordGroup from "../keyWordChipGroup";

const styles = theme => ({
  container: {
    marginLeft: "10vw"
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: "60vw"
  },
  dense: {
    marginTop: 16
  },
  menu: {
    width: 200
  },
  button: {
    verticalAlign: "bottom",
    marginBottom: "10px"
  }
});

class PasteForm extends Component {
  constructor() {
    super();
    this.state = {
      text: "",
      showKeyWord: false,
      keyWordData: ["foo", "bar", "a robot", "meaning", "null"],
      newCoordObject: {}
    };
  }

  onTextChange = event => {
    this.setState({
      ...this.state,
      text: event.target.value
    });
  };

  onButtonClick = () => {
    //prepare your post here which comes
    //console.log("we will post this text now", this.state.text);
    this.setState({ ...this.state, showKeyWord: true });

    if (this.state.text.length >= 5) {
      this.makePost();
    } else {
      alert("der Text is doch ein wenig kurz");
    }
  };

  makePost = () => {
    const url = "http://api.textminer.quving.com";
    let xhr = new XMLHttpRequest();

    xhr.open("POST", url);
    //?
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status <= 300) {
        this.setState({
          ...this.state,
          newCoordObject: JSON.parse(xhr.responseText)
        });
      } else {
        console.log("http error");
      }
    };
    let postOBj = {
      text: this.state.text
    };
    xhr.send(JSON.stringify(postOBj));
  };

  handleDelete = i => {
    console.log("handleDeleteFrom Group", i);
  };

  render() {
    const { classes } = this.props;

    return (
      <>
        <div className={classes.container}>
          <TextField
            id="outlined-multiline-static"
            label="Text"
            multiline
            rows="8"
            className={classes.textField}
            value={this.state.text}
            onChange={this.onTextChange}
            margin="normal"
            variant="outlined"
          />

          <Button
            onClick={this.onButtonClick}
            variant="contained"
            color="primary"
            className={classes.button}
          >
            Senden
          </Button>
        </div>

        {this.state.showKeyWord && (
          <div className={classes.container}>
            <KeyWordGroup
              keywordObj={this.state.keyWordData}
              handleDelete={this.handleDelete}
            />
          </div>
        )}

        <Plot newCoordObject={this.state.newCoordObject} />
      </>
    );
  }
}

PasteForm.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(PasteForm);
