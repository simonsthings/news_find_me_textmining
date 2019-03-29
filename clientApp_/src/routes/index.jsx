import React, { lazy, Suspense } from "react";
import { Route } from "react-router-dom";

/**
 * just a new feature test
 */
const Plot = lazy(() => import("./../components/plot"));
const Start = lazy(() => import("./../components/start"));
const PasteForm = lazy(() => import("./../partials/pasteForm"));

const Router = () => {
  return (
    <>
      <Suspense fallback={<p>preparing your route...</p>}>
        <Route path="/plot" component={Plot} />
        <Route path="/userland" component={PasteForm} />
        <Route path="/" exact component={Start} />
      </Suspense>
    </>
  );
};

export default Router;
