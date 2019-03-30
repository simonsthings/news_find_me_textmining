import React from "react";
import { Link } from "react-router-dom";

import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import IconButton from "@material-ui/core/IconButton";
import MenuIcon from "@material-ui/icons/Menu";

const styles = {
  root: {
    flexGrow: 1
  },
  grow: {
    display: "inline",
    flexGrow: 1,
    margin: "0px 10px"
  },
  link: {
    textDecoration: "none",
    color: "white"
  },
  menuButton: {
    marginLeft: -12,
    marginRight: 20
  }
};

function Header(props) {
  const { classes } = props;
  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Toolbar>
          {false && (
            <IconButton
              className={classes.menuButton}
              color="inherit"
              aria-label="Menu"
            >
              <MenuIcon />
            </IconButton>
          )}

          <div>
            <Typography variant="h6" color="inherit" className={classes.grow}>
              <Link className={classes.link} to="/">
                Start
              </Link>
            </Typography>
            <Typography variant="h6" color="inherit" className={classes.grow}>
              <Link className={classes.link} to="/plot">
                Plot
              </Link>
            </Typography>
            <Typography variant="h6" color="inherit" className={classes.grow}>
              <Link className={classes.link} to="/keywords">
                Keywords
              </Link>
            </Typography>
          </div>
        </Toolbar>
      </AppBar>
    </div>
  );
}

Header.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(Header);
