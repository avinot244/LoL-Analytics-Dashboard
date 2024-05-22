import Modal from "@mui/material/Modal";
import Box from '@mui/material/Box';
import { Button, FormControl, Stack, TextField, Typography } from "@mui/material";
import { API_URL } from "../../constants";
import { useEffect, useState } from "react";
import SystemUpdateAltIcon from '@mui/icons-material/SystemUpdateAlt';
import KeyboardDoubleArrowDownIcon from '@mui/icons-material/KeyboardDoubleArrowDown';

export default function ModalAnalyze({open, handleClose, model}) {
    const [img, setImg] = useState();

    const style = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: "fit-content",
        height : 600,
        bgcolor: 'background.paper',
        border: '2px solid #000',
        boxShadow: 24,
        p: 4,
        overflow: 'scroll'
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
    const n = model.nbFactors;
    const jsonString = model.factorsName.replace(/'/g, '"')
    const factorsName = JSON.parse(jsonString)
    return (
        <Modal
            open={open}
            onClose={handleClose}
        >
            <Box sx={style}>
                <Typography id="modal-modal-title" variant="h6" component="h2"align="center">
                    Loadings of model {model.uuid} for {model.role}
                </Typography>
                <img src={img} alt="model loadings" width={1100} />

                <FormControl defaultValue="" required>
                    <Stack spacing={2} direction="row" justifyContent="center" alignItems="center">
                        {
                            [...Array(n)].map((e, i) => <TextField defaultValue={factorsName[i]} helperText={`Factor ${i+1}`} key={i}/>)            
                        }
                    </Stack>
                </FormControl>
                <Stack spacing={2} direction="row" justifyContent="center" alignItems="center" sx={{mt: 2}}>
                    <Button
                        variant="contained"
                        endIcon={<SystemUpdateAltIcon/>}
                    >
                        Set factors Name
                    </Button>
                    <Button
                        variant="contained"
                        endIcon={<KeyboardDoubleArrowDownIcon/>}
                        color="success"
                    >
                        Set Model
                    </Button>
                    <Button
                        variant="contained"
                        color="error"
                        onClick={() => {
                            handleClose()
                        }}
                    >
                        Close
                    </Button>
                </Stack>
                
            </Box>
            
        </Modal>
    )
}