import { createSlice, PayloadAction } from "@reduxjs/toolkit";

type UserIDState = {
  value: string;
};

const initialState = {
  value: "",
} as UserIDState;

export const slice = createSlice({
  name: "userid",
  initialState,
  reducers: {
    reset: () => initialState,
    setID: (state, action: PayloadAction<string>) => {
      state.value = action.payload;
    },
  },
});

export const {
  setID,
  reset,
} = slice.actions;
export default slice.reducer;
