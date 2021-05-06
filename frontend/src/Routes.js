
import React, { Component } from "react";
import { Router, Switch, Route } from "react-router-dom";

import Analysis from "./pages/Analysis";
import Home from "./pages/Home";
import history from './history';

export default class Routes extends Component {
    render() {
        return (
            <Router history={history}>
                <Switch>
                    <Route path="/" exact component={Home} />
                    <Route path="/Analysis" component={Analysis} />
                </Switch>
            </Router>
        )
    }
}