import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import {Outlet, Link} from "react-router-dom";
import { Button } from '@mui/material';
import { API_URL } from '../constants';



function NavBarComp({loggedIn, setLoggedIn}) {
	function isResponseOk(response) {
        if (response.status >= 200 && response.status <= 299) {
            return response.json();
        }else{
            throw Error(response.statusText)
        }
    }
	function logout() {
		fetch(API_URL + "authentication/logout/", {
			credentials: "same-origin"
		})
		.then(isResponseOk)
		.then((data) => {
			console.log(data)
			setLoggedIn(false)
		})
		.catch((err) => {
			console.log(err)
		})
	}
	

  	return (
    <Navbar data-bs-theme="dark" expand="lg" className="bg-body-tertiary">
      	<Container>
			<Link to="/Home">
				<Navbar.Brand>Aegis DashBoard</Navbar.Brand>
			</Link>
			<Navbar.Toggle aria-controls="basic-navbar-nav" />
			<Navbar.Collapse id="basic-navbar-nav">
			<Nav className="me-auto">
				<Nav.Link as={Link} to="/Home">Home</Nav.Link>

				<NavDropdown title="Champion Overview">
					<NavDropdown.Item as={Link} to='/ChampionOverview/Scrims'>Scrims</NavDropdown.Item>
					<NavDropdown.Item as={Link} to='/ChampionOverview/Esports'>Esports</NavDropdown.Item>
				</NavDropdown>

				<NavDropdown title="Player Overview">
					<NavDropdown.Item as={Link} to='/PlayerOverview/Scrims'>Scrims</NavDropdown.Item>
					<NavDropdown.Item as={Link} to='/PlayerOverview/Esports'>Esports</NavDropdown.Item>
				</NavDropdown>

				<NavDropdown title="Game Overview">
					<NavDropdown.Item as={Link} to='/GameOverview/Scrims'>Scrims</NavDropdown.Item>
					<NavDropdown.Item as={Link} to='/GameOverview/Esports'>Esports</NavDropdown.Item>
				</NavDropdown>

				<NavDropdown title="Monitoring">
					<NavDropdown.Item as={Link} to='/Monitoring/Download'>Download Games</NavDropdown.Item>
					<NavDropdown.Item as={Link} to='/Monitoring/PCAMaker'>PCA Model Maker</NavDropdown.Item>
					<NavDropdown.Item as={Link} to='/Monitoring/PCAOverview'>PCA Model Overview</NavDropdown.Item>
				</NavDropdown>
				

			</Nav>
			</Navbar.Collapse>
      	</Container>
		<Link to="/"><Button variant='contained' sx={{mr: 5}} onClick={() => logout()}>Log Out</Button></Link>
    </Navbar>
  );
}

export default NavBarComp;