import Modal from "@mui/material/Modal";
import Box from '@mui/material/Box';
import { Button, Stack, Typography } from "@mui/material";
import DraftComponentVertical from "../utils/DraftComponentVertical";

import { useEffect, useState } from "react";

import { API_URL } from "../../constants";

export default function RelatedDraftModal({open, handleClose, selected}) {
    const [draftList, setDraftList] = useState([])
    const style = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: "1023px",
        height : "90vh",
        bgcolor: 'background.paper',
        border: '2px solid #000',
        boxShadow: 24,
        p: 4,
        overflow: 'scroll'
    };

    const fetchRelatedDraft = async () => {
        const result = await fetch (API_URL + `draft/getChampion/${selected[0].championName}/${selected[0].patch}/`, {
            method: "GET"
        })
        result.json().then((result) => {
            let newDraftList = result
            setDraftList(newDraftList)
        })
    }

    useEffect(() => {
        fetchRelatedDraft()
    }, [])

    return (
        <Modal
            open={open}
            onClose={handleClose}
        >
            <Box sx={style}>
                <Typography id="modal-modal-title" variant="h2" component="h2"align="center">
                    Related drafts of {selected[0].championName}
                </Typography>
                <br/>

                {draftList.map((draft) => 
                    <>
                        <Typography id="modal-modal-title" variant="h6" component="h5"align="center">
                            {draft.tournament}
                        </Typography>
                        <DraftComponentVertical
                            team1Name={draft.teamBlue}
                            team2Name={draft.teamRed}
                            picksB1rota={[draft.bp1, draft.bp2, draft.bp3]}
                            picksB2rota={[draft.bp4, draft.bp5]}
                            bansB1rota={[draft.bb1, draft.bb2, draft.bb3]}
                            bansB2rota={[draft.bb4, draft.bb5]}
                            picksR1rota={[draft.rp1, draft.rp2, draft.rp3]}
                            picksR2rota={[draft.rp4, draft.rp5]}
                            bansR1rota={[draft.rb1, draft.rb2, draft.rb3]}
                            bansR2rota={[draft.rb4, draft.rb5]}
                            win={draft.winner}
                            championNameFilter={selected[0].championName}
                        />
                    </>
                    
                )}
                <Stack spacing={2} direction="row" justifyContent="center" alignItems="center" sx={{mt: 2}}>
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