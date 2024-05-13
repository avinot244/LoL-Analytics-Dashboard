import NavBarComp from "../NavbarComp";
import "../../styles/PCAModelOverview.css"
import { useState } from "react";
import { API_URL } from "../../constants";

import PCAModelList from "./PCAModelList";

export default function PCAModelOverview() {
    const [modelList, setModelList] = useState([])

    const fetchPCAModels = async () => {
        const result = await fetch(API_URL + `behaviorModels/getAll/`, {
            method: "GET"
        })
        result.json().then(result => {
            console.log(result)
            let newModelList = []
            for (let i = 0; i < result.length ; i++) {
                let modelObject = result[i]
                let temp = {
                    "pk": modelObject.pk,
                    "uuid": modelObject.uuid,
                    "role": modelObject.role,
                    "kmo": (modelObject.kmo).toFixed(2)
                }
                newModelList.push(temp)
            }
            setModelList(newModelList)
        })
    }


    useState(() => {
        fetchPCAModels()
    }, [])

    return (
        <div className="pca-model-overview-wrapper">
            <NavBarComp/>

            <h1>Manage Behavior Analysis Models</h1>
            
            <PCAModelList
                modelList={modelList}
            />

        </div>

    )
}