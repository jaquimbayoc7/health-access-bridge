import { LayoutDashboard, Users, Activity, BarChart3, UserCog, Settings, LogOut, BookOpen } from 'lucide-react';
import { NavLink } from '@/components/NavLink';
import { useLocation } from 'react-router-dom';
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarTrigger,
  useSidebar,
} from '@/components/ui/sidebar';
import { useLanguage } from '@/contexts/LanguageContext';
import { useAuth } from '@/contexts/AuthContext';

const menuItems = [
  { title: 'dashboard', url: '/dashboard', icon: LayoutDashboard },
  { title: 'patients', url: '/patients', icon: Users },
  { title: 'predictions', url: '/predictions', icon: Activity },
  { title: 'analytics', url: '/analytics', icon: BarChart3 },
  { title: 'predictiveGuide', url: '/predictive-guide', icon: BookOpen },
  { title: 'userList', url: '/admin', icon: UserCog },
];

export function AppSidebar() {
  const { state } = useSidebar();
  const location = useLocation();
  const { t } = useLanguage();
  const { logout, user } = useAuth();
  const currentPath = location.pathname;
  const collapsed = state === 'collapsed';

  const isActive = (path: string) => currentPath === path;

  // Filter menu items based on user role
  const filteredMenuItems = menuItems.filter((item) => {
    // Hide patients, predictions, analytics and predictive guide for admin users
    if (user?.role === 'admin' && ['patients', 'predictions', 'analytics', 'predictiveGuide'].includes(item.title)) {
      return false;
    }
    // Hide admin panel for non-admin users
    if (user?.role !== 'admin' && item.title === 'userList') {
      return false;
    }
    return true;
  });

  return (
    <Sidebar className={collapsed ? 'w-14' : 'w-60'} collapsible="icon">
      <SidebarContent className="pt-4">
        {!collapsed && (
          <div className="px-6 py-4">
            <h2 className="text-xl font-bold text-primary">Health Access Bridge</h2>
          </div>
        )}
        
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              {filteredMenuItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <NavLink
                      to={item.url}
                      end
                      className="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors hover:bg-sidebar-accent"
                      activeClassName="bg-primary text-primary-foreground hover:bg-primary-hover"
                    >
                      <item.icon className="h-5 w-5 flex-shrink-0" />
                      {!collapsed && <span className="font-medium">{t(item.title)}</span>}
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <div className="mt-auto border-t border-sidebar-border">
          <SidebarGroup>
            <SidebarGroupContent>
              <SidebarMenu>
                <SidebarMenuItem>
                  <SidebarMenuButton asChild>
                    <NavLink
                      to="/settings"
                      className="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors hover:bg-sidebar-accent"
                      activeClassName="bg-primary text-primary-foreground"
                    >
                      <Settings className="h-5 w-5 flex-shrink-0" />
                      {!collapsed && <span className="font-medium">{t('settings')}</span>}
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
                <SidebarMenuItem>
                  <SidebarMenuButton onClick={logout}>
                    <div className="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors hover:bg-sidebar-accent cursor-pointer">
                      <LogOut className="h-5 w-5 flex-shrink-0" />
                      {!collapsed && <span className="font-medium">{t('logout')}</span>}
                    </div>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        </div>
      </SidebarContent>
    </Sidebar>
  );
}
