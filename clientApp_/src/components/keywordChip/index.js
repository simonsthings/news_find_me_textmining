import React, { Component } from "react";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import Chip from "@material-ui/core/Chip";

const styles = theme => ({
  root: {
    display: "flex",
    justifyContent: "center",
    flexWrap: "wrap"
  },
  chip: {
    margin: theme.spacing.unit
  }
});

class KeyWordChip extends Component {
  handleDelete = i => {
    console.log("delete chip w/o store?");
    alert(`delete ${this.props.label}`);
  };

  render() {
    const { label, classes } = this.props;
    return (
      <Chip
        label={label}
        onDelete={this.handleDelete}
        className={classes.chip}
        color="primary"
      />
    );
  }
}

KeyWordChip.propTypes = {
  classes: PropTypes.object.isRequired,
  label: PropTypes.string,
  handleDelete: PropTypes.func
};

export default withStyles(styles)(KeyWordChip);
