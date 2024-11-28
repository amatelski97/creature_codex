import { type MRT_TableInstance } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    open: boolean;
    table: MRT_TableInstance<TData>;
}
export declare const MRT_EditRowModal: <TData extends Record<string, any> = {}>({ open, table, }: Props<TData>) => import("react/jsx-runtime").JSX.Element;
export {};
