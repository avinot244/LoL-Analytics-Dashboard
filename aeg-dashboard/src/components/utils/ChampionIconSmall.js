import { useState, useEffect, useContext } from "react";
import "../../styles/ChampionIconSmall.css"
import AuthContext from "../context/AuthContext";

function ChampionIconSmall({championName, width, height}) {
    console.log(championName)
    let {patch} = useContext(AuthContext)
    const apiURL = `https://ddragon.leagueoflegends.com/cdn/${patch}/img/champion/${championName}.png`
    const [img, setImg] = useState();

    const fetchImage = async () => {
        const res = await fetch(apiURL);
        const imageBlob = await res.blob();
        const imageObjectURL = URL.createObjectURL(imageBlob);
        setImg(imageObjectURL);
    };

    useEffect(() => {
        fetchImage();
    }, []);



    return (
        <img className="champion-icon-small" src={img} alt={championName} width={width} height={height}/>
    )


    
}

export default ChampionIconSmall;