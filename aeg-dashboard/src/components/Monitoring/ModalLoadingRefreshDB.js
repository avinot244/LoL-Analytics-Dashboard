import Modal from "@mui/material/Modal";

import { Typography, Box, Stack, CircularProgress } from "@mui/material";

export default function ModalLoadingRefreshDB({open, handleClose, dbName}){
    const style = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: "fit-content",
        height : "200px",
        bgcolor: 'background.paper',
        border: '2px solid #000',
        boxShadow: 24,
        p: 4
    };

    return (
        <Modal
            open={open}
            onClose={handleClose}
        >
            <Box sx={style}>
                <Typography id="modal-refreshdb-title" variant="h6" component="h2"align="center">
                        Updating {dbName} database... Please Wait
                </Typography>
                <br/>
                <Stack spacing={2} direction="row" justifyContent="center" alignItems="center" sx={{pb: 2}}>
                    <CircularProgress />
                </Stack>
            </Box>
        </Modal>
    )
}