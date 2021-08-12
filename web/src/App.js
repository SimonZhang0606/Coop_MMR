import "./App.css";
import {
  BrowserRouter as Router,
  Route,
  Switch,
  withRouter,
} from "react-router-dom";
import Jobs from "./Jobs.js";
import Job from "./Job.js";
import Companies from "./Companies.js";
import Company from "./Company.js";
// import {Navbar, Nav, NavDropdown} from 'react-bootstrap';
// import Container from 'react-bootstrap/Container';
import { Navbar, Nav } from "react-bootstrap";

const Header = (props) => {
  const { location } = props;
  return (
    <Navbar bg="none" variant="light" expand="lg">
      <Navbar.Brand href="/">Coop MMR</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto" activeKey={location.pathname}>
          <Nav.Link href="/">🏢 Companies</Nav.Link>
          <Nav.Link href="/jobs">💼 Jobs</Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

const HeaderWithRouter = withRouter(Header);

function App() {
  return (
    <>
      <Router>
        <HeaderWithRouter />
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
