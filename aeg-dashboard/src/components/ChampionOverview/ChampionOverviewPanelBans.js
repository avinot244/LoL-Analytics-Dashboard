import * as React from 'react';
import PropTypes from 'prop-types';
import { alpha } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import TableSortLabel from '@mui/material/TableSortLabel';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Checkbox from '@mui/material/Checkbox';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import SearchIcon from '@mui/icons-material/Search';
import { visuallyHidden } from '@mui/utils';
import { API_URL } from '../../constants';
import RelatedDraftModal from './RelatedDraftModal';

import AuthContext from '../context/AuthContext';
import ChampionIconSmall from '../utils/ChampionIconSmall';

function descendingComparator(a, b, orderBy) {
    if (b[orderBy] < a[orderBy]) {
        return -1;
    }
    if (b[orderBy] > a[orderBy]) {
        return 1;
    }
    return 0;
}

function getComparator(order, orderBy) {
    return order === 'desc'
        ? (a, b) => descendingComparator(a, b, orderBy)
        : (a, b) => -descendingComparator(a, b, orderBy);
}

// Since 2020 all major browsers ensure sort stability with Array.prototype.sort().
// stableSort() brings sort stability to non-modern browsers (notably IE11). If you
// only support modern browsers you can replace stableSort(exampleArray, exampleComparator)
// with exampleArray.slice().sort(exampleComparator)
function stableSort(array, comparator) {
    const stabilizedThis = array.map((el, index) => [el, index]);
    stabilizedThis.sort((a, b) => {
        const order = comparator(a[0], b[0]);
        if (order !== 0) {
            return order;
        }
        return a[1] - b[1];
    });
    return stabilizedThis.map((el) => el[0]);
}
const headCells = [
    {
        id: 'championName',
        numeric: false,
        disablePadding: true,
        label: 'Champion Name',
    },
    {
        id: 'globalBanRate',
        numeric: true,
        disablePadding: false,
        label: 'Ban Rate',
    },
    {
        id: 'banRate1Rota',
        numeric: true,
        disablePadding: false,
        label: 'Ban Rate 1st  Rotation',
    },
    {
        id: 'banRate2Rota',
        numeric: true,
        disablePadding: false,
        label: 'Ban Rate 2nd  Rotation',
    },
];

function EnhancedTableHead(props) {
    const { onSelectAllClick, order, orderBy, numSelected, rowCount, onRequestSort } = props;
    const createSortHandler = (property) => (event) => {
        onRequestSort(event, property);
    };

    return (
        <TableHead>
            <TableRow>
                <TableCell padding="checkbox">
                    <Checkbox
                        color="primary"
                        indeterminate={numSelected > 0 && numSelected < rowCount}
                        checked={rowCount > 0 && numSelected === rowCount}
                        onChange={onSelectAllClick}
                        inputProps={{
                            'aria-label': 'select all Champions',
                        }}
                    />
                </TableCell>

                {headCells.map((headCell) => (
                    <TableCell
                        key={headCell.id}
                        align={headCell.numeric ? 'right' : 'left'}
                        padding={headCell.disablePadding ? 'none' : 'normal'}
                        sortDirection={orderBy === headCell.id ? order : false}
                    >
                        <TableSortLabel
                            active={orderBy === headCell.id}
                            direction={orderBy === headCell.id ? order : 'asc'}
                            onClick={createSortHandler(headCell.id)}
                        >
                            {headCell.label}
                            {orderBy === headCell.id ? (
                                <Box component="span" sx={visuallyHidden}>
                                    {order === 'desc' ? 'sorted descending' : 'sorted ascending'}
                                </Box>
                            ) : null}
                        </TableSortLabel>
                    </TableCell>
                ))}
            </TableRow>
        </TableHead>
    );
}

EnhancedTableHead.propTypes = {
    numSelected: PropTypes.number.isRequired,
    onRequestSort: PropTypes.func.isRequired,
    onSelectAllClick: PropTypes.func.isRequired,
    order: PropTypes.oneOf(['asc', 'desc']).isRequired,
    orderBy: PropTypes.string.isRequired,
    rowCount: PropTypes.number.isRequired,
};

function EnhancedTableToolbar(props) {
    const [open, setOpen] = React.useState(false)
    

    const { numSelected, selected } = props;

    return (
        <Toolbar
        sx={{
            pl: { sm: 2 },
            pr: { xs: 1, sm: 1 },
            ...(numSelected > 0 && {
                bgcolor: (theme) =>
                    alpha(theme.palette.primary.main, theme.palette.action.activatedOpacity),
            }),
        }}
        >

            <Typography
                sx={{ flex: '1 1 100%' }}
                variant="h6"
                id="tableTitle"
                component="div"
            >
                Champion bans
            </Typography>

        </Toolbar>
    );
}

EnhancedTableToolbar.propTypes = {
    numSelected: PropTypes.number.isRequired,
    selected: PropTypes.array.isRequired
};

export default function ChampionOverviewPanelBans(props) {
    const {value, panelIndex, tournament, patch, side} = props
    const [order, setOrder] = React.useState('asc');
    const [orderBy, setOrderBy] = React.useState('championName');
    const [selected, setSelected] = React.useState([]);
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(10);
    
    
    const [wantedRows, setRows] = React.useState([])

    const roleList = ["Top", "Jungle", "Mid", "ADC", "Support"]
    let {authTokens} = React.useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }

    React.useEffect(() => {
        const fetchChampionsDraftStats = async (tournament, patch, side) => {
            const result = await fetch(API_URL + `draft/championStats/getBans/${patch}/${side}/${tournament}/`, {
                method: "GET",
                headers:header
            })
            result.json().then(result => {
                const newData = result;

                let newWantedRows = []
                newData.map((championDraftStats) => {
                    if (championDraftStats.mostPopularRole === roleList[panelIndex]) {
                        newWantedRows.push(championDraftStats)
                    }
                })
                if (panelIndex > 4) {
                    setRows(newData)
                } else {
                    setRows(newWantedRows)   
                }
            })
        }
        

        fetchChampionsDraftStats(tournament, patch, side)
    }, [])

    const handleRequestSort = (event, property) => {
        const isAsc = orderBy === property && order === 'asc';
        setOrder(isAsc ? 'desc' : 'asc');
        setOrderBy(property);
    };

    const handleSelectAllClick = (event) => {
        if (event.target.checked) {
            const newSelected = wantedRows.map((n) => n.pk);
            setSelected(newSelected);
            return;
        }
        setSelected([]);
    };

    const handleClick = (event, object) => {
        const selectedIndex = selected.indexOf(object);
        let newSelected = [];

        if (selectedIndex === -1) {
            newSelected = newSelected.concat(selected, object);
        } else if (selectedIndex === 0) {
            newSelected = newSelected.concat(selected.slice(1));
        } else if (selectedIndex === selected.length - 1) {
            newSelected = newSelected.concat(selected.slice(0, -1));
        } else if (selectedIndex > 0) {
            newSelected = newSelected.concat(
                selected.slice(0, selectedIndex),
                selected.slice(selectedIndex + 1),
            );
        }
        setSelected(newSelected);
    };

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    const isSelected = (object) => selected.indexOf(object) !== -1;

    // Avoid a layout jump when reaching the last page with empty rows.
    const emptyRows =
        page > 0 ? Math.max(0, (1 + page) * rowsPerPage - wantedRows.length) : 0;

    
    const visibleRows = stableSort(wantedRows, getComparator(order, orderBy)).slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
    // const visibleRows = React.useMemo(
    //     () => stableSort(wantedRows, getComparator(order, orderBy)).slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage),
    //     [order, orderBy, page, rowsPerPage],
    // );
    return (
        <>
            {
                panelIndex === 5 &&
                <div className='wrapper-tabpanel-championOverview'>
                    <div 
                        role='tabpanbel'
                        hidden={value !== panelIndex}
                        className={`simple-tabpanel-${panelIndex}`}
                        aria-labelledby={`simple-tab-${panelIndex}`}
                    >
                        <Typography id="PCAdocumentation-title" variant="h4" component="h4" align="center" sx={{mt: 10}}>
                            Only Banned Champions
                        </Typography>
                        <Box sx={{ width: '100%', paddingTop: 3 }}>
                        <Paper sx={{ width: '100%', mb: 2 }}>
                            <EnhancedTableToolbar 
                                numSelected={selected.length}
                                selected={selected}

                            />
                            <TableContainer>
                            <Table
                                sx={{ minWidth: 750 }}
                                aria-labelledby="tableTitle"
                                size={'small'}
                            >
                                <EnhancedTableHead
                                    numSelected={selected.length}
                                    order={order}
                                    orderBy={orderBy}
                                    onSelectAllClick={handleSelectAllClick}
                                    onRequestSort={handleRequestSort}
                                    rowCount={wantedRows.length}
                                />
                                <TableBody>
                                {visibleRows.map((row, index) => {
                                    const isItemSelected = isSelected(row);
                                    const labelId = `enhanced-table-checkbox-${index}`;

                                    return (
                                    <TableRow
                                        hover
                                        onClick={(event) => handleClick(event, row)}
                                        role="checkbox"
                                        aria-checked={isItemSelected}
                                        tabIndex={-1}
                                        key={row.id}
                                        selected={isItemSelected}
                                        sx={{ cursor: 'pointer' }}
                                    >
                                        <TableCell padding="checkbox">
                                        <Checkbox
                                            color="primary"
                                            checked={isItemSelected}
                                            inputProps={{
                                                'aria-labelledby': labelId,
                                            }}
                                        />
                                        </TableCell>
                                        <TableCell
                                            component="th"
                                            id={labelId}
                                            scope="row"
                                            padding="none"
                                        >
                                            {row.championName}
                                            {/* <ChampionIconSmall 
                                                championName={row.championName} 
                                                width={50} 
                                                height={50}
                                            /> */}
                                        </TableCell>
                                        <TableCell align="right">{(row.globalBanRate*100).toFixed(2)}%</TableCell>
                                        <TableCell align="right">{(row.banRate1Rota*100).toFixed(2)}%</TableCell>
                                        <TableCell align="right">{(row.banRate2Rota*100).toFixed(2)}%</TableCell>
                                    </TableRow>
                                    );
                                })}
                                {emptyRows > 0 && (
                                    <TableRow
                                    style={{
                                        height: 33 * emptyRows,
                                    }}
                                    >
                                    <TableCell colSpan={6} />
                                    </TableRow>
                                )}
                                </TableBody>
                            </Table>
                            </TableContainer>
                            <TablePagination
                                rowsPerPageOptions={[5, 10, 25]}
                                component="div"
                                count={wantedRows.length}
                                rowsPerPage={rowsPerPage}
                                page={page}
                                onPageChange={handleChangePage}
                                onRowsPerPageChange={handleChangeRowsPerPage}
                            />
                        </Paper>
                        </Box>
                    </div>
                </div>
            }
        </>
    );
}