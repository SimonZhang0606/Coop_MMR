import './App.css';
import { BrowserRouter as Router, Route, Switch, Link, useLocation } from 'react-router-dom';
import Jobs from './Jobs.js';
import Job from './Job.js';
import Companies from './Companies.js';
import Company from './Company.js'

function App() {
  return (
    <>
      <Router>
        <div class="header">
          <h1 class="title">Coop MMR</h1>
          <Link to="/" class="header-button"> 
              <p>Companies</p>
          </Link>
          <Link to="/jobs" class="header-button"> 
              <p>Jobs</p>
          </Link>
        </div>
        <Switch>
          <Route path="/jobs" component={Jobs} />
          <Route exact path="/job/:jid" component={Job} />
          <Route exact path="/company/:cid" component={Company} />
          <Route exact path="/" component={Companies} />
        </Switch>
      </Router>
    </>
  );
}

export default App;
