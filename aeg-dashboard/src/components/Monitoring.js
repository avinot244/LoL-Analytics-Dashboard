import * as React from 'react';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import Button from '@mui/material/Button';

import '../styles/Monitoring.css'

import NavBarComp from './NavbarComp';
import SearchComp from './SearchComp';

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    pt: 2,
    px: 4,
    pb: 3,
};

function ChildModal() {
    const [open, setOpen] = React.useState(false);
    const handleOpen = () => {
        setOpen(true);
    };
    const handleClose = () => {
        setOpen(false);
    };

    return (
        <React.Fragment>
        <Button onClick={handleOpen} variant="contained">Open Child Modal</Button>
        <Modal
            open={open}
            onClose={handleClose}
            aria-labelledby="child-modal-title"
            aria-describedby="child-modal-description"
        >
            <Box sx={{ ...style, width: 200 }}>
            <h2 id="child-modal-title">Text in a child modal</h2>
            <p id="child-modal-description">
                Lorem ipsum, dolor sit amet consectetur adipisicing elit.
            </p>
            <Button onClick={handleClose} variant='contained' color='error'>Close Child Modal</Button>
            </Box>
        </Modal>
        </React.Fragment>
    );
}

export default function Monitoring() {
    const [open, setOpen] = React.useState(false);
    const [selectedElement, setSelectedElement] = React.useState();
    const handleOpen = () => {
        setOpen(true);
    };
    const handleClose = () => {
        setOpen(false);
    };

    return (
        <div className='wrapper-Monitoring'>
        <NavBarComp/>

        <h1>Monitoring</h1>
        <SearchComp
            elementList={["Aymeric", "Vinot", "Aegis", "Aymeric", "Vinot", "Aegis"]}
            setSelectedElement={setSelectedElement}
        />

        <Button
            onClick={handleOpen}
            variant='contained'
        >
            Open modal
        </Button>
        <Modal
            open={open}
            onClose={handleClose}
            aria-labelledby="parent-modal-title"
            aria-describedby="parent-modal-description"
        >
            <Box sx={{ ...style, width: 400 }}>
                <h2 id="parent-modal-title">Text in a modal</h2>
                <p id="parent-modal-description">
                    Duis mollis, est non commodo luctus, nisi erat porttitor ligula.
                </p>
                <Button
                    onClick={handleClose}
                    variant='contained'
                    color='error'
                >
                    Close Modal    
                </Button>
                <ChildModal />
            </Box>
        </Modal>
        </div>
    );
}