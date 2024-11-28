import { type MRT_TableInstance } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    table: MRT_TableInstance<TData>;
}
export declare const MRT_ToolbarInternalButtons: <TData extends Record<string, any> = {}>({ table, }: Props<TData>) => import("react/jsx-runtime").JSX.Element;
export {};
