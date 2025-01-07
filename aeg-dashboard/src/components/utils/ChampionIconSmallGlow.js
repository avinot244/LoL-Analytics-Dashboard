import { useEffect, useState, useContext } from "react";
import "../../styles/ChampionIconSmall.css"

function ChampionIconSmallGlow({championName, width, height, glow}) {
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