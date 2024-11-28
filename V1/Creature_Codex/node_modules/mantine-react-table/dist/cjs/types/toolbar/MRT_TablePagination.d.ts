import { type MRT_TableInstance } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    position?: 'top' | 'bottom';
    table: MRT_TableInstance<TData>;
}
export declare const MRT_TablePagination: <TData extends Record<string, any> = {}>({ table, position, }: Props<TData>) => import("react/jsx-runtime").JSX.Element;
export {};
