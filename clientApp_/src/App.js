import React, { Component } from "react";
import { BrowserRouter } from "react-router-dom";

import Router from "./routes";
import Header from "./components/header";
import "./App.css";

class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <Header />
        <Router />
      </BrowserRouter>
    );
  }
}

export default App;
