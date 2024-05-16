import Modal from "@mui/material/Modal";
import Box from '@mui/material/Box';
import { Button, Typography } from "@mui/material";
import { API_URL } from "../../constants";
import { useEffect, useState } from "react";

export default function ModalAnalyze({open, handleClose, model}) {
    const [img, setImg] = useState();

    const style = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: "fit-content",
        bgcolor: 'background.paper',
        border: '2px solid #000',
        boxShadow: 24,
        p: 4,
    };

    const fetchLoadingMatrix = async () => {
        const res = await fetch(API_URL + `behaviorModels/getLoadingMatrix/${model.uuid}/${model.role}/`)
        const imageBlob = await res.blob()
        const imageObjectURL = URL.createObjectURL(imageBlob)
        setImg(imageObjectURL)
    }

    useState(() => {
        fetchLoadingMatrix();
    }, [])

    console.log(model)

    return (
        <Modal
            open={open}
            onClose={handleClose}
        >
            <Box sx={style}>
                <Typography id="modal-modal-title" variant="h6" component="h2">
                    Loadings of model {model.uuid} for {model.role}
                </Typography>
                <img src={img} alt="model loadings" width={1100} />
                <Button
                    variant="contained"
                    color="error"
                    onClick={() => {
                        handleClose()
                    }}
                >
                    Close
                </Button>
            </Box>
            
        </Modal>
    )
}