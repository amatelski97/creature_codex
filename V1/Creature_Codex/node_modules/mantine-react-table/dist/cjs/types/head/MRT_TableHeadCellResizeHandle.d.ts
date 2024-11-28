import { type MRT_Header, type MRT_TableInstance } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    header: MRT_Header<TData>;
    table: MRT_TableInstance<TData>;
}
export declare const MRT_TableHeadCellResizeHandle: <TData extends Record<string, any> = {}>({ header, table, }: Props<TData>) => import("react/jsx-runtime").JSX.Element;
export {};
