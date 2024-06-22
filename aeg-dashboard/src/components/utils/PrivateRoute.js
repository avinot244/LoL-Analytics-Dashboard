import { Outlet, Navigate } from "react-router-dom";
import { useContext } from "react";
import AuthContext from "../context/AuthContext";

const PrivateRoute = ({children, ...rest}) => {
    let {user} = useContext(AuthContext)
    let bool = user !== null
    return (
        bool ? <Outlet /> : <Navigate to="/"/>
    )
}
export default PrivateRoute