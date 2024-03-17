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

				<NavDropdown title="Champion Overview">
					<NavDropdown.Item href='/ChampionOverview/Scrims'>Scrims</NavDropdown.Item>
					<NavDropdown.Item href='/ChampionOverview/Esports'>Esports</NavDropdown.Item>
				</NavDropdown>

				<NavDropdown title="Player Overview">
					<NavDropdown.Item as={Link} to='/PlayerOverview/Scrims'>Scrims</NavDropdown.Item>
					<NavDropdown.Item href='/PlayerOverview/Esports'>Esports</NavDropdown.Item>
				</NavDropdown>

				<NavDropdown title="Game Overview">
					<NavDropdown.Item href='/GameOverview/Scrims'>Scrims</NavDropdown.Item>
					<NavDropdown.Item href='/GameOverview/Esports'>Esports</NavDropdown.Item>
				</NavDropdown>
				
				{/* <NavDropdown title="Game Overview" id="basic-nav-dropdown">		
					<NavDropdown.Item href="#action/3.1">Post-game stats</NavDropdown.Item>
					<NavDropdown.Item href="#action/3.2">Another action</NavDropdown.Item>
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