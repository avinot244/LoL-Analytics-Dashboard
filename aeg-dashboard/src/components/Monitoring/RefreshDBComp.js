import ModalLoadingRefreshDB from "./ModalLoadingRefreshDB";
import AuthContext from "../context/AuthContext";
import NavBarComp from "../utils/NavbarComp"
import "../../styles/RefreshDBComp.css"
import { API_URL } from "../../constants";

import { useState, useContext } from "react";

import { Typography, Stack, Button } from "@mui/material"
import RefreshIcon from '@mui/icons-material/Refresh';

export default function RefreshDBComp() {
    const [loadingBehavior, setLoadingBehavior] = useState(false)
    const [loadingDrafts, setLoadingDrafts] = useState(false)
    const [loadingGameMetadata, setLoadingGameMetadata] = useState(false)

    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }

    const refreshDatabaseDrafts = async () => {
        const result = await fetch(API_URL + `monitoring/refresh/drafts/`, {
            method: "PATCH",
            headers: header
        })
        if (result.status === 200) {
            setLoadingDrafts(false)
        }
    }

    const refreshDatabaseBehavior = async () => {
        const result = await fetch(API_URL + `monitoring/refresh/behavior/`, {
            method: "PATCH",
            headers: header
        })
        if (result.status === 200) {
            setLoadingBehavior(false)
        }
    }

    const refreshDatabaseGames = async () => {
        const result = await fetch(API_URL + `monitoring/refresh/games/`, {
            method: "PATCH",
            headers: header
        })
        if (result.status === 200) {
            setLoadingGameMetadata(true)
        }
    }
    return (
        <div className="wrapper-refresh-db">
            <NavBarComp />
            <Typography id="PCAdocumentation-title" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                Refresh Databases
            </Typography>
            

            <Stack spacing={2} direction="row" alignItems="center" justifyContent="center" sx={{mt: 10}}>
                <Button
                    variant="contained"
                    endIcon={<RefreshIcon/>}
                    onClick={() => {
                        setLoadingBehavior(true);
                        refreshDatabaseBehavior()
                    }}
                >
                    Refresh Behavior
                </Button>

                <ModalLoadingRefreshDB
                    open={loadingBehavior}
                    handleClose={setLoadingBehavior}
                    dbName="Behavior"
                />
                

                <Button
                    variant="contained"
                    endIcon={<RefreshIcon/>}
                    onClick={() => {
                        setLoadingDrafts(true);
                        refreshDatabaseDrafts()
                    }}
                >
                    Refresh Drafts
                </Button>

                <ModalLoadingRefreshDB
                    open={loadingDrafts}
                    handleClose={setLoadingDrafts}
                    dbName="Drafts"
                />


                <Button
                    variant="contained"
                    endIcon={<RefreshIcon/>}
                    onClick={() => {
                        setLoadingGameMetadata(true);
                        refreshDatabaseGames()
                    }}
                >
                    Refresh Game Metadata
                </Button>

                <ModalLoadingRefreshDB
                    open={loadingGameMetadata}
                    handleClose={setLoadingGameMetadata}
                    dbName="Game Metadata"
                />
            </Stack>
        </div>
    )
}