import Modal from "@mui/material/Modal";
import Box from '@mui/material/Box';
import { Button, FormControl, Stack, TextField, Typography } from "@mui/material";
import { API_URL } from "../../constants";
import { useEffect, useRef, useState } from "react";
import SystemUpdateAltIcon from '@mui/icons-material/SystemUpdateAlt';
import KeyboardDoubleArrowDownIcon from '@mui/icons-material/KeyboardDoubleArrowDown';

import PCADbOverview from "./PCADbOverview";

import "../../styles/PCAModalAnalyze.css"



export default function ModalAnalyze({open, handleClose, model, flag, setFlag, setSelected}) {
    const [img, setImg] = useState();
    const [regionSplit, setRegionSplit] = useState({})
    const textFieldRefs = useRef([]);

    const style = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: "fit-content",
        height : "90vh",
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
    
    const fetchRegionSplit = async () => {
        const dict = await fetch(API_URL + `behaviorModels/getRegionSplit/${model.uuid}/${model.role}/`)
        dict.json().then((regionSplit) => {
            let newRegionSplit = regionSplit
            setRegionSplit(newRegionSplit)
        })
    }

    const setModelActive = async () => {
        const res = await fetch(API_URL + `behaviorModels/setActive/${model.uuid}/${model.role}/`,{
            method: "PATCH"
        })
        const temp = flag + 1
        setFlag(temp)
        setSelected([])
        handleClose()
    }

    


    const setFactorsNameCall = async () => {
        const currentValues = textFieldRefs.current.map(ref => ref.value);
        const res = await fetch(API_URL + `behaviorModels/setFactorsName/${model.uuid}/${model.role}/`, {
            method: "PATCH",
            body: JSON.stringify(currentValues)
        })
    }

    useEffect(() => {
        fetchLoadingMatrix();
        fetchRegionSplit();
    }, [])

    const n = model.nbFactors;
    const jsonString = model.factorsName.replace(/'/g, '"')
    let factorsNameTemp = JSON.parse(jsonString)
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
                
                <div className="wrapper-pcamodal-piechart">
                    <PCADbOverview
                        regionSplit={regionSplit}
                    />
                </div>
                

                <FormControl defaultValue="" required>
                    <Stack spacing={2} direction="row" justifyContent="center" alignItems="center">
                        {
                            [...Array(n)].map((e, i) => 
                                <TextField 
                                    defaultValue={factorsNameTemp[i]} 
                                    helperText={`Factor ${i+1}`} 
                                    key={i}
                                    inputRef={el => textFieldRefs.current[i] = el}
                                    variant="outlined"
                                />
                            )            
                        }
                    </Stack>
                </FormControl>
                <Stack spacing={2} direction="row" justifyContent="center" alignItems="center" sx={{mt: 2}}>
                    <Button
                        variant="contained"
                        endIcon={<SystemUpdateAltIcon/>}
                        onClick={() => {
                            setFactorsNameCall()
                        }}
                    >
                        Set factors Name
                    </Button>
                    <Button
                        variant="contained"
                        endIcon={<KeyboardDoubleArrowDownIcon/>}
                        color="success"
                        onClick={ () => {
                            setModelActive()
                        }}
                    >
                        Set Model
                    </Button>
                    <Button
                        variant="contained"
                        color="error"
                        onClick={() => {
                            const temp = flag + 1
                            setFlag(temp)
                            setSelected([])
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