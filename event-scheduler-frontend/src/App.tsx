import { useEffect, useState } from "react";
import axios from "axios";
import { Card, CardContent } from "./components/ui/card";
import { Button } from "./components/ui/button";
import { Dialog, DialogTrigger, DialogContent, DialogTitle } from "./components/ui/dialog";
import { Input } from "./components/ui/input";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "./components/ui/select";
import { ChevronLeft, ChevronRight } from "lucide-react";
import dayjs from "dayjs";
import { VisuallyHidden } from "@radix-ui/react-visually-hidden";
import { DialogDescription } from "@radix-ui/react-dialog";


const api = axios.create({
  baseURL: "http://localhost:8000/api",
});

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [relativeN, setRelativeN] = useState("");
  const [RelativeDayOrInterval, setRelativeDayOrInterval] = useState("");
  const [RelativeTimeframe, setRelativeTimeframe] = useState("");
  const [IntervalTimeframe, setIntervalTimeframe] = useState("");
  const [IntervalN, setIntervalN] = useState("");
  const [WeekdayChoice, setWeekdayChoice]=useState("");
  const [bookedDates, setBookedDates] = useState("");
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));
  const [showAddEventForm, setShowAddEventForm] = useState(false);
  const [recurrenceType, setRecurrenceType] = useState("one time");
  const [currentDate, setCurrentDate] = useState(dayjs());  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [eventsOnSelectedDate, setEventsOnSelectedDate] = useState<EventItem[]>([]);
  const [myEvents, setMyEvents] = useState<EventItem_[]>([]);
  const [eventName, setEventName] = useState("");
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [showDialog, setShowDialog] = useState(false);
  const [isRegisterMode, setIsRegisterMode] = useState(false);


  type EventItem = {
    id: number;
    EventName: string;
    Time: string;
    date: string;
  
  };

  type EventItem_ = {
    id: number;
    event_name: string;
    time: string;
    date: string;
    recursion_type:string;
  };



  useEffect(() => {
    if (token) {
      api.defaults.headers.common["Authorization"] = `Token ${token}`;
      setIsAuthenticated(true);
    }
    fetchCalendar();
  }, [token]);

      const fetchCalendar = async () => {
      try {
        const res = await api.get("/calendar");
        console.log("Calendar API response:", res.data);
        const booked = res.data
          .map((day: any) => day.date);
        setBookedDates(booked);
      } catch (err) {
        console.error("Failed to fetch calendar grid:", err);
      }
    };


  const handleRegister = async () => {
  try {
    const res = await api.post("/register", {
      username,
      password,
    });
    alert("Registered successfully. You can now log in.");
    setIsRegisterMode(false);
  } catch (err) {
    console.error("Registration failed:", err);
    alert("Registration failed. Username may already exist.");
  }
};

  const handleLogin = async () => {
    try {
      const res = await api.post("/login", { username, password });
      const t = res.data.token;
      setToken(t);
      localStorage.setItem("token", t);
      setIsAuthenticated(true);
    } catch (error) {
      alert("Invalid credentials");
    }
  };

  const handleLogout = () => {
    setToken(null);
    setIsAuthenticated(false);
    localStorage.removeItem("token");
    delete api.defaults.headers.common["Authorization"];
  };
  
  const handleMyEvents = async () => {
    try {
        const res = await api.get("/events");
        setMyEvents(res.data);
    } catch (error) {
        console.error("Failed to fetch my events:", error);
        alert("Could not load your events");
      }
  };

  const handleCreate = async () => {
    const payload: any = {
      event_name: eventName,
      time:time,
      date:date,
      recursion_type: recurrenceType,
    };
    
    if (date) payload.date = date;

    if (recurrenceType === "interval" && IntervalN && IntervalTimeframe) {
      payload.interval_n = parseInt(IntervalN);
      payload.interval_timeframe = IntervalTimeframe;
    }

    if (recurrenceType === "weekday" && WeekdayChoice) {
      payload.weekday_choice = parseInt(WeekdayChoice);
    }

    if (recurrenceType === "relative" && relativeN && RelativeDayOrInterval && RelativeTimeframe) {
      payload.relative_n = isNaN(Number(relativeN)) ? relativeN : parseInt(relativeN);
      payload.relative_day_or_interval = RelativeDayOrInterval;
      payload.relative_timeframe = RelativeTimeframe;
    }

    try {
      console.log(payload);
      await api.post("/create", payload);
      alert("Event created");
      window.location.reload();
    } catch (err:any) {
      console.error(err.response?.data);
      alert("Creation failed");
    }
  };

  const handleUpdate = async (e: number) => {
    const payload: any = {
      event_name: eventName,
      time:time,
      date:date,
      recursion_type: recurrenceType,
    };
    
    if (date) payload.date = date;

    if (recurrenceType === "interval" && IntervalN && IntervalTimeframe) {
      payload.interval_n = parseInt(IntervalN);
      payload.interval_timeframe = IntervalTimeframe;
    }

    if (recurrenceType === "weekday" && WeekdayChoice) {
      payload.weekday_choice = parseInt(WeekdayChoice);
    }

    if (recurrenceType === "relative" && relativeN && RelativeDayOrInterval && RelativeTimeframe) {
      payload.relative_n = isNaN(Number(relativeN)) ? relativeN : parseInt(relativeN);
      payload.relative_day_or_interval = RelativeDayOrInterval;
      payload.relative_timeframe = RelativeTimeframe;
    }

    try {
      console.log(payload);
      await api.put(`/update/${e}`, payload);
      alert("Event updated");
      window.location.reload()
    } catch (err:any) {
      console.error(err.response?.data);
      alert("Update failed");
    }
  };

  const handleDayClick = async (d: string) => {
    try {
      const res = await api.get(`/events_on_specific_day/${d}`);
      console.log("Fetched events:", res.data);
      setSelectedDate(d);
      setEventsOnSelectedDate(res.data);
      setShowDialog(true)
    } catch (err:any) {
      console.error(err.response?.data)
      alert("Failed to load events for selected date");
    }
  };

  const deleteOccurrence = async (id: number) => {
    try {
      await api.delete(`/delete_occurence/${id}/`);
      alert("Event occurrence deleted");
      setEventsOnSelectedDate(prev => prev.filter(e => e.id !== id));
      fetchCalendar();
    } catch (err) {
      console.error("Delete failed:", err);
      alert("Failed to delete occurrence");
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await api.delete(`/delete/${id}/`);
      alert("Event deleted");
      setEventsOnSelectedDate(prev => prev.filter(e => e.id !== id));
      fetchCalendar()
    } catch (err) {
      console.error("Delete failed:", err);
      alert("Failed to delete event");
    }
  };

  const startOfMonth = currentDate.startOf("month");
  const daysInMonth = currentDate.daysInMonth();
  const firstDayOffset = startOfMonth.day();

  const dates = Array.from({ length: firstDayOffset + daysInMonth }, (_, i) =>
    i < firstDayOffset ? null : dayjs(startOfMonth).add(i - firstDayOffset, "day")
  );

  const handlePrevMonth = () => {
    if (currentDate.year() > 2025 || (currentDate.year() === 2025 && currentDate.month() > 0)) {
      setCurrentDate(currentDate.subtract(1, "month"));
    }
  };

  const handleNextMonth = () => {
    if (currentDate.year() < 2030 || (currentDate.year() === 2030 && currentDate.month() < 11)) {
      setCurrentDate(currentDate.add(1, "month"));
    }
  };

  

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      {!isAuthenticated ? (
      <div className="max-w-md mx-auto mt-20 bg-white shadow rounded p-6">
          <h2 className="text-xl font-bold mb-4">
            {isRegisterMode ? "Register" : "Login"}
          </h2>

          <Input
            placeholder="Username"
            className="mb-2"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <Input
            placeholder="Password"
            type="password"
            className="mb-4"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <Button
            onClick={isRegisterMode ? handleRegister : handleLogin}
            className="w-full mb-2"
          >
            {isRegisterMode ? "Register" : "Login"}
          </Button>

          <p className="text-sm text-center">
            {isRegisterMode ? (
              <>
                Already have an account?{" "}
                <button
                  className="text-blue-500 underline"
                  onClick={() => setIsRegisterMode(false)}
                >
                  Login
                </button>
              </>
            ) : (
              <>
                Don’t have an account?{" "}
                <button
                  className="text-blue-500 underline"
                  onClick={() => setIsRegisterMode(true)}
                >
                  Register
                </button>
              </>
            )}
          </p>
        </div>
      ) : (
        <div>
          <div className="flex justify-between items-center mb-4">
            <div className="space-x-2 flex items-center">
              <Dialog>
                <DialogTrigger asChild>
                  <Button onClick={() => handleMyEvents()}>My Events</Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogTitle><VisuallyHidden>Title</VisuallyHidden></DialogTitle>
                  <DialogDescription><VisuallyHidden>Description</VisuallyHidden></DialogDescription>
                  <h3 className="font-bold mb-2">My Events</h3>
                  {myEvents.length > 0 && (
                      <div className="mt-4">
                        <h2 className="text-lg font-semibold mb-2">My Events</h2>
                        <ul className="space-y-1">
                          {myEvents.map(event => (
                            <li key={event.id}>
                            <span> 📌 <strong>{event.event_name}</strong> — {event.date} @ {event.time} </span>
                                <div className="flex gap-2">
                                  <Dialog>
                                    <DialogTrigger asChild>
                                      <button
                                    //onClick={() => handleEdit(event)}
                                    className="text-blue-500 hover:text-blue-700 text-xs"
                                  >
                                    Edit
                                  </button>
                                    </DialogTrigger>
                                    <DialogContent>
                                      <DialogTitle><VisuallyHidden>Title</VisuallyHidden></DialogTitle>
                                      <DialogDescription><VisuallyHidden>Description</VisuallyHidden></DialogDescription>
                                      <h3 className="font-bold mb-4">Edit Event</h3>
                                      <Input value={eventName} onChange={(e) => setEventName(e.target.value)}placeholder="Event Name" className="mb-2" />
                                      <Input value={date} onChange={(e) => setDate(e.target.value)}type="date" className="mb-2" />
                                      <Input value={time} onChange={(e) => setTime(e.target.value)}type="time" className="mb-2" />

                                      <Select onValueChange={setRecurrenceType} value={recurrenceType}>
                                        <SelectTrigger className="mb-2">
                                          <SelectValue placeholder="Recurrence Type" />
                                        </SelectTrigger>
                                        <SelectContent>
                                          <SelectItem value="one_time">One time</SelectItem>
                                          <SelectItem value="daily">Daily</SelectItem>
                                          <SelectItem  value="weekly">Weekly</SelectItem>
                                          <SelectItem  value="monthly">Monthly</SelectItem>
                                          <SelectItem  value="interval">Interval</SelectItem>
                                          <SelectItem  value="weekday">Weekday (eg. Every Friday)</SelectItem>
                                          <SelectItem  value="relative">Relative (eg. Every 2nd tuesday of the month/year)</SelectItem>
                                        </SelectContent>
                                      </Select>

                                      {recurrenceType === "interval" && (
                                        <div className="mb-2 space-y-2">
                                          <Input value = {IntervalN} onChange={(e) => setIntervalN(e.target.value)} placeholder="Interval number" />
                                          <Select onValueChange={(value) => setIntervalTimeframe(value)}>
                                            <SelectTrigger>
                                              <SelectValue placeholder="Interval unit" />
                                            </SelectTrigger>
                                            <SelectContent>
                                              {['day', 'week', 'month', 'year'].map(unit => (
                                                <SelectItem key={unit} value={unit}>{unit}</SelectItem>
                                              ))}
                                            </SelectContent>
                                          </Select>
                                        </div>
                                      )}

                                      {recurrenceType === "weekday" && (
                                        <Select onValueChange={(value) => setWeekdayChoice(value)}>
                                          <SelectTrigger className="mb-2">
                                            <SelectValue placeholder="Weekday"/>
                                          </SelectTrigger>
                                          <SelectContent>
                                            <SelectItem value="1">Monday</SelectItem>
                                            <SelectItem value="2">Tuesday</SelectItem>
                                            <SelectItem value="3">Wednesday</SelectItem>
                                            <SelectItem value="4">Thursday</SelectItem>
                                            <SelectItem value="5">Friday</SelectItem>
                                            <SelectItem value="6">Saturday</SelectItem>
                                            <SelectItem value="7">Sunday</SelectItem>
                                          </SelectContent>
                                        </Select>
                                      )}

                                      {recurrenceType === "relative" && (
                                        <div className="mb-2 space-y-2">
                                          <Input placeholder="Rank (eg. 1, 2 or last)" value={relativeN} onChange={(e) => setRelativeN(e.target.value)} />
                                          <Select onValueChange={(value) => setRelativeDayOrInterval(value)}>
                                            <SelectTrigger>
                                              <SelectValue placeholder="Day option" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem  value="1">Monday</SelectItem>
                                                <SelectItem value="2">Tuesday</SelectItem>
                                                <SelectItem  value="3">Wednesday</SelectItem>
                                                <SelectItem  value="4">Thursday</SelectItem>
                                                <SelectItem value="5">Friday</SelectItem>
                                                <SelectItem  value="6">Saturday</SelectItem>
                                                <SelectItem  value="7">Sunday</SelectItem>
                                                <SelectItem  value="weekday">Weekday</SelectItem>
                                                <SelectItem  value="weekend">Weekend day (eg. Sat or Sun)</SelectItem>
                                            </SelectContent>
                                          </Select>
                                          <Select onValueChange={(value) => setRelativeTimeframe(value)}>
                                            <SelectTrigger>
                                              <SelectValue placeholder="Month or Year" />
                                            </SelectTrigger>
                                            <SelectContent>
                                              {["month", "year"].map(unit => (
                                                <SelectItem key={unit} value={unit}>{unit}</SelectItem>
                                              ))}
                                            </SelectContent>
                                          </Select>
                                        </div>
                                      )}

                          

                                      <Button className="w-full" onClick={() => handleUpdate(event.id)}>Update</Button>
                                    </DialogContent>
                                  </Dialog>
                                  
                                  <button
                                    onClick={() => handleDelete(event.id)}
                                    className="text-red-500 hover:text-red-700 text-xs"
                                  >
                                    Delete
                                  </button>
                                </div>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                </DialogContent>
              </Dialog>

              <Dialog>
                <DialogTrigger asChild>
                  <Button onClick={() => setShowAddEventForm(true)}>Add Event</Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogTitle><VisuallyHidden>Title</VisuallyHidden></DialogTitle>
                  <DialogDescription><VisuallyHidden>Description</VisuallyHidden></DialogDescription>
                  <h3 className="font-bold mb-4">Create Event</h3>
                  <Input value={eventName} onChange={(e) => setEventName(e.target.value)}placeholder="Event Name" className="mb-2" />
                  <Input value={date} onChange={(e) => setDate(e.target.value)}type="date" className="mb-2" />
                  <Input value={time} onChange={(e) => setTime(e.target.value)}type="time" className="mb-2" />

                  <Select onValueChange={setRecurrenceType} value={recurrenceType}>
                    <SelectTrigger className="mb-2">
                      <SelectValue placeholder="Recurrence Type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="one_time">One time</SelectItem>
                      <SelectItem value="daily">Daily</SelectItem>
                      <SelectItem  value="weekly">Weekly</SelectItem>
                      <SelectItem  value="monthly">Monthly</SelectItem>
                      <SelectItem  value="interval">Interval</SelectItem>
                      <SelectItem  value="weekday">Weekday (eg. Every Friday)</SelectItem>
                      <SelectItem  value="relative">Relative (eg. Every 2nd tuesday of the month/year)</SelectItem>
                    </SelectContent>
                  </Select>

                  {recurrenceType === "interval" && (
                    <div className="mb-2 space-y-2">
                      <Input value = {IntervalN} onChange={(e) => setIntervalN(e.target.value)} placeholder="Interval number" />
                      <Select onValueChange={(value) => setIntervalTimeframe(value)}>
                        <SelectTrigger>
                          <SelectValue placeholder="Interval unit" />
                        </SelectTrigger>
                        <SelectContent>
                          {['day', 'week', 'month', 'year'].map(unit => (
                            <SelectItem key={unit} value={unit}>{unit}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  )}

                  {recurrenceType === "weekday" && (
                    <Select onValueChange={(value) => setWeekdayChoice(value)}>
                      <SelectTrigger className="mb-2">
                        <SelectValue placeholder="Weekday"/>
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="1">Monday</SelectItem>
                        <SelectItem value="2">Tuesday</SelectItem>
                        <SelectItem value="3">Wednesday</SelectItem>
                        <SelectItem value="4">Thursday</SelectItem>
                        <SelectItem value="5">Friday</SelectItem>
                        <SelectItem value="6">Saturday</SelectItem>
                        <SelectItem value="7">Sunday</SelectItem>
                      </SelectContent>
                    </Select>
                  )}

                  {recurrenceType === "relative" && (
                    <div className="mb-2 space-y-2">
                      <Input placeholder="Rank (eg. 1, 2 or last)" value={relativeN} onChange={(e) => setRelativeN(e.target.value)} />
                      <Select onValueChange={(value) => setRelativeDayOrInterval(value)}>
                        <SelectTrigger>
                          <SelectValue placeholder="Day option" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem  value="1">Monday</SelectItem>
                            <SelectItem value="2">Tuesday</SelectItem>
                            <SelectItem  value="3">Wednesday</SelectItem>
                            <SelectItem  value="4">Thursday</SelectItem>
                            <SelectItem value="5">Friday</SelectItem>
                            <SelectItem  value="6">Saturday</SelectItem>
                            <SelectItem  value="7">Sunday</SelectItem>
                            <SelectItem  value="weekday">Weekday</SelectItem>
                            <SelectItem  value="weekend">Weekend day (eg. Sat or Sun)</SelectItem>
                        </SelectContent>
                      </Select>
                      <Select onValueChange={(value) => setRelativeTimeframe(value)}>
                        <SelectTrigger>
                          <SelectValue placeholder="Month or Year" />
                        </SelectTrigger>
                        <SelectContent>
                          {["month", "year"].map(unit => (
                            <SelectItem key={unit} value={unit}>{unit}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  )}

                  <Button className="w-full" onClick={handleCreate}>Create</Button>
                </DialogContent>
              </Dialog>
              
            </div>
            <Button onClick={handleLogout}>Logout</Button>
          </div>

          <Card className="max-w-4xl mx-auto">
            <CardContent className="p-4">
              <div className="flex justify-between items-center mb-4">
                <Button variant="ghost" onClick={handlePrevMonth}><ChevronLeft /></Button>
                <div className="text-xl font-bold">{currentDate.format("MMMM YYYY")}</div>
                <Button variant="ghost" onClick={handleNextMonth}><ChevronRight /></Button>
              </div>
              <div className="grid grid-cols-7 w-full text-center text-sm font-semibold text-gray-600 mb-2">
                {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((day) => (
                  <div key={day}>{day}</div>
                ))}
              </div>
              <div className="grid grid-cols-7 gap-2">
                {dates.map((date, idx) => (
                  <div key={idx} className="h-20 border rounded flex items-center justify-center relative">
                    {date ? (
                      <Dialog>
                        <DialogTrigger asChild>
                          <button
                            className="w-full h-full flex items-center justify-center relative"
                            onClick={() => {
                              const formattedDate = date.format("YYYY-MM-DD");
                              setSelectedDate(formattedDate);
                              handleDayClick(formattedDate);
                            }}
                          >
                            {date.date()}
                            {bookedDates.includes(date.format("YYYY-MM-DD")) && (
                              <span className="absolute bottom-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
                            )}
                          </button>
                        </DialogTrigger>
                        <DialogContent>
                          <DialogTitle><VisuallyHidden>Title</VisuallyHidden></DialogTitle>
                          <DialogDescription><VisuallyHidden>Description</VisuallyHidden></DialogDescription>
                          <h3 className="font-bold mb-2">Events on {selectedDate}</h3>
                          
                            <DialogDescription>
                              {eventsOnSelectedDate.length === 0 ? (
                                <p className="text-gray-500 italic">No events on this date.</p>
                              ) : (
                                <ul className="space-y-2">
                                  {eventsOnSelectedDate.map((event: any) => (
                                    <li key={event.id} className="text-sm">
                                      <span>
                                        📌 <strong>{event.EventName}</strong> @ {event.Time}
                                      </span>
                                      <button
                                        onClick={() => deleteOccurrence(event.id)}
                                        className="text-red-500 hover:text-red-700 text-xs"
                                      >
                                        Delete
                                      </button>
                                    </li>
                                    
                                  ))}
                                </ul>
                              )}
                            </DialogDescription>
                        </DialogContent>
                      </Dialog>
                    ) : null}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}


