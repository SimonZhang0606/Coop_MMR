import './App.css';
import { BrowserRouter as Router, Route, Switch, Link, useLocation } from 'react-router-dom';
import Jobs from './Jobs.js';
import Companies from './Companies.js';
import Company from './Company.js'

function App() {
  return (
    <>
      <Router>
        <h1>Coop MMR</h1>
        <Link to="/"> 
          <p>Companies</p>
        </Link>
        <Link to="/jobs"> 
          <p>Jobs</p>
        </Link>
        <Switch>
          <Route path="/jobs" component={Jobs} />
          <Route exact path="/company/:cid" component={Company} />
          <Route exact path="/" component={Companies} />
        </Switch>
      </Router>
    </>
  );
}

export default App;
