import { Switch } from "@mui/material";
import { purple } from '@mui/material/colors';
import { alpha, styled } from '@mui/material/styles';

const PurpleSwitch = styled(Switch)(({ theme }) => ({
    '& .MuiSwitch-switchBase.Mui-checked': {
        color: purple[600],
        '&:hover': {
            backgroundColor: alpha(purple[600], theme.palette.action.hoverOpacity),
        },
    },
    '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
        backgroundColor: purple[600],
    },
}));

export default PurpleSwitch