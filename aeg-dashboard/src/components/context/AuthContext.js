import { createContext, useState, useEffect } from "react";
import { API_URL } from "../../constants";
import { jwtDecode } from "jwt-decode";
import { redirect, useNavigate } from "react-router-dom";

const AuthContext = createContext()

export default AuthContext

export const AuthProvider = ({children}) => {
    let [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null)
    let [user, setUser] = useState(() => localStorage.getItem('authTokens') ? jwtDecode(localStorage.getItem('authTokens')) : null)
    let [loading, setLoading] = useState(true)
    let [patch, setPatch] = useState("")

    const getPatch = async () => {
        const result = await fetch("https://ddragon.leagueoflegends.com/api/versions.json")
        if (result.status == 200) {
            let patchList = await result.json()
            const newPatch = patchList[0]
            setPatch(newPatch)
            console.log(newPatch)
        }else {
            console.log("Unable to retrieve data from DDragon API")
        }
    }

    const login = async (userName, password) => {

        // Make a post request to login api
        let result = await fetch(API_URL + "token/getPair/", {
            method: "POST",
            headers: {
                "Content-type": "application/json",
            },
            body: JSON.stringify({'username':userName, 'password':password})
        })
        let data = await result.json()
        console.log(result.status)
        if (result.status === 200) {
            setAuthTokens(data)
            setUser(jwtDecode(data.access))
            localStorage.setItem('authTokens', JSON.stringify(data))
            return true
        }else {
            return false
        }
    }

    const logoutUser = () => {
        setAuthTokens(null)
        setUser(null)
        localStorage.removeItem('authTokens')
    }

    let updateToken = async () => {
        console.log("Token updated !")
        let result = await fetch(API_URL + "token/refresh/", {
            method: "POST",
            headers: {
                "Content-type": "application/json",
            },
            body: JSON.stringify({'refresh': authTokens.refresh})
        })
        let data = await result.json()
        if (result.status === 200) {
            setAuthTokens(data)
            setUser(jwtDecode(data.access))
            localStorage.setItem('authTokens', JSON.stringify(data))
        } else {
            logoutUser()
        }
    }

    let contextData = {
        user:user,
        authTokens:authTokens,
        patch:patch,
        login:login,
        logoutUser:logoutUser,
        
    }

    useEffect(() => {
        getPatch()
        let interval = setInterval(() => {
            if (authTokens) {
                updateToken()
            }
        }, 240000)
        return () => clearInterval(interval)
    }, [authTokens, loading])

    return (
        <AuthContext.Provider value={contextData} >
            {children}
        </AuthContext.Provider>
    )
}
