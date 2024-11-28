import { type MRT_Header, type MRT_TableInstance } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    header: MRT_Header<TData>;
    rangeFilterIndex?: number;
    table: MRT_TableInstance<TData>;
}
export declare const MRT_FilterTextInput: <TData extends Record<string, any> = {}>({ header, rangeFilterIndex, table, }: Props<TData>) => import("react/jsx-runtime").JSX.Element;
export {};
