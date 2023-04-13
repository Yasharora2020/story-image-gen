import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import StoryPage from './StoryPage';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/story/:storyId" component={StoryPage} />
      </Switch>
    </Router>
  );
}

export default App;
