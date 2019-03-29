import React, { Component } from "react";
import { BrowserRouter, Route, Link } from "react-router-dom";
import Plot from "./plot";
import Start from "./start";
import Userland from "./interact";
import "./App.css";

class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <header>
          <Link to="/">Start</Link>
          <Link to="/plot">Plot</Link>
          <Link to="/userland">Userland</Link>
        </header>

        <div className="app">
          <Route path="/plot" component={Plot} />
          <Route path="/userland" component={Userland} />
          <Route path="/" exact component={Start} />
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
