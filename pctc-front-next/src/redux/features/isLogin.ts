import { createSlice, PayloadAction } from "@reduxjs/toolkit";

type IsLoginState = {
  value: boolean;
};

const initialState = {
  value: false,
} as IsLoginState;

export const slice = createSlice({
  name: "islogin",
  initialState,
  reducers: {
    reset: () => initialState,
    setIsLogin: (state, action: PayloadAction<boolean>) => {
      state.value = action.payload;
    },
  },
});

export const {
  setIsLogin,
  reset,
} = slice.actions;
export default slice.reducer;
