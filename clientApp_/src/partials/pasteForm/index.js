import React, { Component } from "react";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";

import KeyWordGroup from "../keyWordChipGroup";
//const KeyWordGroup = lazy(() => import("../keyWordChipGroup"));

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
      keyWordData: ["foo", "bar", "a robot", "meaning", "null"]
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
    console.log("we will post this text now", this.state.text);
    this.setState({ ...this.state, showKeyWord: true });
  };

  handleDelete = i => {
    console.log("handleDeleteFrom Group", i);
  };

  render() {
    const { classes } = this.props;
    console.log(this.state);

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
          <div>
            <KeyWordGroup
              keywordObj={this.state.keyWordData}
              handleDelete={this.handleDelete}
            />
          </div>
        )}
      </>
    );
  }
}

PasteForm.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(PasteForm);
