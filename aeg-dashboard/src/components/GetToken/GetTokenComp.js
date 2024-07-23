import { useState } from "react";

import NavBarComp from "../utils/NavbarComp";
import "../../styles/GetToken.css"
import Typography from '@mui/material/Typography';
import AuthContext from "../context/AuthContext";
import { useContext } from "react";
import { Button } from "@mui/material";
import DownloadIcon from '@mui/icons-material/Download';
import FileDownloadDoneIcon from '@mui/icons-material/FileDownloadDone';
import { API_URL } from "../../constants";

function CopyButton ({content, buttonText, onClick, state, setState}) {
    let bool = true
    let copyToClipboard = () => {
        navigator.clipboard.writeText(content)
            .catch(err => {
                console.err("Failed to copy text: ", err)
            })
    }

    let clearClipBoard = () => {
        navigator.clipboard.writeText("")
            .catch(err => {
                console.log("Failed to copy text: ", err)
            })
    }
    
    if (state) {
        return (
            <Button 
                variant="contained" 
                onClick={() => {
                    onClick();
                    clearClipBoard()
                    setState(state ^ true)
                }}
                startIcon={<FileDownloadDoneIcon/>}
                sx={{
                    ml:5
                }}
            >
                {buttonText}
            </Button>
        )
    } else {
        return (
            <Button 
                variant="contained" 
                onClick={() => {
                    onClick();
                    copyToClipboard();
                    setState(state ^ true)
                }}
                startIcon={<DownloadIcon/>}
                sx={{
                    ml:5
                }}
            >
                {buttonText}
            </Button>
        )
    }
}

export default function GetTokenComp () {
    let {authTokens} = useContext(AuthContext)
    const [textAccess, setTextAccess] = useState("Get Access Token")
    const [textRefresh, setTextRefresh] = useState("Get Refresh Token")

    const [accessState, setAccessState] = useState(false)
    const [refreshState, setRefreshState] = useState(false)



    let onClickAccess = () => {
        if (!accessState) {
            setTextAccess("Access token copied to clipboard !")
            setAccessState(true)
        }else {
            setTextAccess("Get Access Token")
            setAccessState(false)
        }
        
    }

    let onClickRefresh = () => {
        if (!refreshState) {
            setTextRefresh("Access token copied to clipboard !")
            setRefreshState(true)
        }else {
            setTextRefresh("Get Access Token")
            setRefreshState(false)
        }
        
    }


    const sendRequest = async () => {
        const header = {
            Authorization: "Bearer " + authTokens.access
        }

        let result = await fetch(API_URL + "authentication/test", {
            method: "GET",
            headers: header
        })

        if (result.status === 200) {
            alert("Ok !")
        }
    }

    
    return (
        <div className="wrapper-getToken">
            <NavBarComp />
            <div className="wrapper-content-token">
                <Typography id="PCAdocumentation-title" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                    Get Your Tokens
                </Typography>

                <Typography color={"error"} variant="h4">They refresh every 4 mins</Typography>
                <Typography variant="h5" className="tokens-values">
                    Access Token : 
                </Typography>
                <CopyButton 
                    content={authTokens.access} 
                    buttonText={textAccess}
                    onClick={onClickAccess}
                    state={accessState}
                    setState={setAccessState}
                />
            </div>
        </div>
    )
}