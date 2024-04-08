import sys,os
base_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(__file__))
from .form import Form
from .switch import Switch
from .shareList import ShareList
from .icon import Icon
from .table import Table
from .browseBox import BrowseBox
from .scope import Scope
from .button import Button
from .dialog import Dialog
from .tips import Tips
from .menu import Menu
from .checkbox import Checkbox
from .selectUi import SelectUi
from .anchorList import AnchorList
from .batchoperator import Batchoperator
from .board import Board
from .breadCrumb import BreadCrumb
from .calendarUi import CalendarUi
from .cascader import Cascader
from .cityPicker import CityPicker
from .collapse import Collapse
from .commentUi import CommentUi
from .dateMenuUi import DateMenu
from .datePickerUi import DatePickerUi
from .dateQuickFilterUi import DateQuickFilterUi
from .timePickerUi import TimePickerUi
from .dateTimePickerUi import DateTimePickerUi
from .empty import Empty
from .inputUi import InputUi
from .intro import Intro
from .listOp import ListOp
from .monthDayPickerUi import MonthDayPickerUi
from .pickerViewUi import PickerViewUi
from .popover import Popover
from .radio import Radio
from .rate import Rate
from .richText import RichText
from .rightMenu import RightMenu
from .selectGroup import SelectGroup
from .slider import Slider
from .spin import Spin
from .steps import Steps
from .tag import Tag
from .timelineUi import TimelineUi
from .title import Title
from .transfer import Transfer
from .tree import Tree
from .trigger import Trigger
from .upload import Upload

class components(
    AnchorList,
    Icon,
    Menu,
    Checkbox,
    SelectUi,
    Table,
    Scope,
    Button,
    Dialog,
    Switch,
    Tips,
    InputUi,
    Board,
    BreadCrumb,
    CalendarUi,
    CityPicker,
    Collapse,
    CommentUi,
    DateMenu,
    DatePickerUi,
    DateQuickFilterUi,
    TimePickerUi,
    DateTimePickerUi,
    Empty,
    Intro,
    ListOp,
    MonthDayPickerUi,
    PickerViewUi,
    Popover,
    Radio,
    Rate,
    RichText,
    RightMenu,
    SelectGroup,
    Slider,
    Spin,
    Steps,
    Tag,
    TimelineUi,
    Title,
    Transfer,
    Tree,
    Trigger,
    Upload,
    BrowseBox,
    Batchoperator,
    Cascader,
    ShareList,
    Form,
):
    pass