import { useState, useEffect } from "react";
import "../../styles/ChampionIconSmall.css"

function ChampionIconSmallGlow({championName, width, height, glow}) {
    const apiURL = `https://ddragon.leagueoflegends.com/cdn/14.13.1/img/champion/${championName}.png`
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

    if (glow) {
        return (

            <img className="champion-icon-small-glow" src={img} alt={championName} width={width} height={height}/>
    
        )
    } else {
        return (

            <img className="champion-icon-small" src={img} alt={championName} width={width} height={height}/>
    
        )
    }

    
}

export default ChampionIconSmallGlow;