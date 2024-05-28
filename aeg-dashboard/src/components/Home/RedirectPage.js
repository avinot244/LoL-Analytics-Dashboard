import { Button } from '@mui/material';
import { Link } from "react-router-dom";
import Nav from 'react-bootstrap/Nav';
export default function RedirectPage() {
    return (
        <>
            <h1>You are not allowed to access this page without authentication</h1>
            <h2>Please log in</h2>
            <Button
                variant='contained'
            >
                <Nav.Link as={Link} to="/">Go to Login page</Nav.Link>
            </Button>
        </>
    )
}