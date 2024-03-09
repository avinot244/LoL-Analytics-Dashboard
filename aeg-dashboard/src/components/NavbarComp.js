import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import "../styles/NavbarComp.css"
import {Outlet, Link} from "react-router-dom";

function NavBarComp() {
  return (
    <Navbar data-bs-theme="dark" expand="lg" className="bg-body-tertiary">
      	<Container>
			<Link to="/">
				<Navbar.Brand>Aegis DashBoard</Navbar.Brand>
			</Link>
			<Navbar.Toggle aria-controls="basic-navbar-nav" />
			<Navbar.Collapse id="basic-navbar-nav">
			<Nav className="me-auto">
				<Nav.Link as={Link} to="/">Home</Nav.Link>
				<Nav.Link as={Link} to="/ChampionOverview">Champion Overview</Nav.Link>
				<Nav.Link as={Link} to="/PlayerOverview">Player Overview</Nav.Link>
				<Nav.Link as={Link} to="/GameOverview">Game Overview</Nav.Link>
				
				{/* <NavDropdown title="Game Overview" id="basic-nav-dropdown">		
				<NavDropdown.Item href="#action/3.1">Post-game stats</NavDropdown.Item>
				<NavDropdown.Item href="#action/3.2">
					Another action
				</NavDropdown.Item>
				<NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
				<NavDropdown.Divider />
				<NavDropdown.Item href="#action/3.4">
					Separated link
				</NavDropdown.Item>
				</NavDropdown> */}

			</Nav>
			</Navbar.Collapse>
      	</Container>
    </Navbar>
  );
}

export default NavBarComp;