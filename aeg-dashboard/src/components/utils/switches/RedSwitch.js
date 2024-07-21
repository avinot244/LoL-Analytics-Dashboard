import { Switch } from "@mui/material";
import { red } from '@mui/material/colors';
import { alpha, styled } from '@mui/material/styles';

const RedSwitch = styled(Switch)(({ theme }) => ({
    '& .MuiSwitch-switchBase.Mui-checked': {
        color: red[600],
        '&:hover': {
            backgroundColor: alpha(red[600], theme.palette.action.hoverOpacity),
        },
    },
    '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
        backgroundColor: red[600],
    },
}));
export default RedSwitch